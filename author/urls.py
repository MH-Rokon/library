from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegistrationAPIView,
    ActivateAccountAPIView,  
    LoginAPIView,
    ProfileAPIView, 
    LogoutAPIView,
    PasswordResetRequestAPIView,
    PasswordResetConfirmAPIView,
)

app_name = "author"

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateAccountAPIView.as_view(), name='activate-account'), 
    path('login/', LoginAPIView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('reset-password-request/', PasswordResetRequestAPIView.as_view(), name='reset-password-request'),
    path('reset-password-confirm/<uidb64>/<token>/', PasswordResetConfirmAPIView.as_view(), name='reset-password-confirm'),
]
