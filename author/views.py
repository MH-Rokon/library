from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .serializers import UserSerializer

User = get_user_model()

# User registration endpoint
class RegistrationAPIView(APIView):
    serializer_class = serializers.RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_link = f"https://library-uniy.onrender.com/api/activate/{uid}/{token}/"

            subject = "Activate Your Account"
            message = f"Welcome! Activate your account by clicking this link:\n\n{activation_link}"

            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                user.delete()
                return Response(
                    {"error": f"Failed to send confirmation email: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                {"detail": "Registration successful. Please check your email to activate your account."},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Account activation endpoint
class ActivateAccountAPIView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({"error": "Invalid activation link."}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_active:
            return Response({"detail": "Account already activated."}, status=status.HTTP_200_OK)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"detail": "Account activated successfully."}, status=status.HTTP_200_OK)

        return Response({"error": "Activation link is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)

# User login endpoint
class LoginAPIView(APIView):
    serializer_class = serializers.UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user:
                if not user.is_active:
                    return Response({"error": "Account not active. Please verify your email."}, status=status.HTTP_403_FORBIDDEN)

                refresh = RefreshToken.for_user(user)

                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user_id': user.id
                }, status=status.HTTP_200_OK)

            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User profile retrieval
class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

# User logout endpoint
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

# Password reset request
class PasswordResetRequestAPIView(APIView):
    serializer_class = serializers.PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"detail": "If this email is registered, you will receive a password reset email."})

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"https://library-uniy.onrender.com/api/reset-password-confirm/{uid}/{token}/"

            subject = "Password Reset Request"
            message = (
                f"Hi,\n\nYou requested a password reset. Click below to reset your password:\n\n"
                f"{reset_link}\n\nIf you didn’t request this, ignore this email."
            )

            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
            except Exception as e:
                return Response(
                    {"error": f"Failed to send reset email: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response({"detail": "If this email is registered, you will receive a password reset link."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Password reset confirmation
class PasswordResetConfirmAPIView(APIView):
    serializer_class = serializers.PasswordResetConfirmSerializer

    def post(self, request, uidb64, token):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user = User.objects.get(pk=uid)
            except (User.DoesNotExist, ValueError, TypeError, OverflowError):
                return Response({"error": "Invalid reset link."}, status=status.HTTP_400_BAD_REQUEST)

            if not default_token_generator.check_token(user, token):
                return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data['new_password'])
            user.save()

            return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
