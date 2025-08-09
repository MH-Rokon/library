from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from .models import Borrow
from .serializers import BorrowSerializer, BorrowCreateSerializer
from django.contrib.auth import get_user_model
from book.models import Book
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

# Borrow book endpoint
class BorrowBookAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = BorrowCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            book_id = serializer.validated_data['book_id']
            active_borrows_count = Borrow.objects.filter(user=user, return_date__isnull=True).count()
            if active_borrows_count >= 3:
                return Response({"error": "Borrowing limit reached (max 3 active books)."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                book = Book.objects.select_for_update().get(id=book_id)
            except Book.DoesNotExist:
                return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

            if book.available_copies < 1:
                return Response({"error": "No available copies of this book."}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                book.available_copies -= 1
                book.save()

                borrow = Borrow.objects.create(
                    user=user,
                    book=book,
                    borrow_date=timezone.now(),
                    due_date=timezone.now() + timedelta(days=14)
                )

            return Response(BorrowSerializer(borrow).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# List user borrows
class ListUserBorrowsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        active_borrows = Borrow.objects.filter(user=user, return_date__isnull=True)
        serializer = BorrowSerializer(active_borrows, many=True)
        return Response(serializer.data)

# Return borrowed book
class ReturnBookAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        borrow_id = request.data.get('borrow_id')
        if not borrow_id:
            return Response({"error": "borrow_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            borrow = Borrow.objects.select_for_update().get(id=borrow_id, user=request.user)
        except Borrow.DoesNotExist:
            return Response({"error": "Borrow record not found"}, status=status.HTTP_404_NOT_FOUND)

        if borrow.return_date:
            return Response({"error": "Book already returned"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            borrow.return_date = timezone.now()
            borrow.save()

            book = borrow.book
            book.available_copies += 1
            book.save()

            days_late = (borrow.return_date - borrow.due_date).days
            if days_late > 0:
                user_profile = request.user.profile  
                user_profile.penalty_points += days_late
                user_profile.save()

        return Response({"detail": f"Book returned. Late by {max(days_late, 0)} days. Penalty points updated."})

# User penalty points
class UserPenaltyPointsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        if request.user.id != id and not request.user.is_staff:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        penalty_points = user.profile.penalty_points  
        return Response({"user_id": id, "penalty_points": penalty_points})

# Email due notifications
class Command(BaseCommand):
    help = "Send due date email notifications to users for borrows due today"

    def handle(self, *args, **kwargs):
        today = now().date()
        borrows_due_today = Borrow.objects.filter(due_date=today, return_date__isnull=True)

        for borrow in borrows_due_today:
            user = borrow.user
            book = borrow.book
            subject = f"Reminder: Book '{book.title}' is due today"
            message = (
                f"Hello {user.username},\n\n"
                f"Your borrowed book '{book.title}' is due today ({today}). Please return it on time to avoid penalty points.\n\n"
                "Thank you for using our Library Management System."
            )

            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
                self.stdout.write(self.style.SUCCESS(f"Sent email to {user.email} for '{book.title}'"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to send email to {user.email}: {e}"))
