from django.urls import path
from .views import (
    AuthorListCreateAPIView,
    CategoryListCreateAPIView,
    BookListAPIView,
    BookDetailAPIView,
    BookCreateAPIView,
    BookUpdateAPIView,
    BookDeleteAPIView,
)

urlpatterns = [
    path('authors/', AuthorListCreateAPIView.as_view(), name='author-list-create'),
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('books/', BookListAPIView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail'),
    path('books/create/', BookCreateAPIView.as_view(), name='book-create'),   
    path('books/<int:pk>/update/', BookUpdateAPIView.as_view(), name='book-update'),  
    path('books/<int:pk>/delete/', BookDeleteAPIView.as_view(), name='book-delete'), 
]
