from rest_framework import serializers
from .models import Borrow
from book.models import Book

class BorrowSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = Borrow
        fields = ['id', 'book', 'book_title', 'borrow_date', 'due_date', 'return_date']

class BorrowCreateSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()

    def validate_book_id(self, value):
        try:
            book = Book.objects.get(pk=value)
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book does not exist.")
        if book.available_copies < 1:
            raise serializers.ValidationError("No available copies of this book.")
        return value
