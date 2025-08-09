from django.urls import path
from .views import (
    BorrowBookAPIView,
    ListUserBorrowsAPIView,
    ReturnBookAPIView,
    UserPenaltyPointsAPIView,
)
app_name = "borrow"

urlpatterns = [
    path('book/', BorrowBookAPIView.as_view(), name='borrow-book'),
    path('book/list/', ListUserBorrowsAPIView.as_view(), name='list-borrows'),
    path('return/', ReturnBookAPIView.as_view(), name='return-book'),
    path('users/<int:id>/penalties/', UserPenaltyPointsAPIView.as_view(), name='user-penalties'),
]
