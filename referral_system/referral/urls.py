from django.urls import path
from .views import PhoneNumberLoginView, OTPVerificationView, UserProfileView

urlpatterns = [
    path('login/', PhoneNumberLoginView.as_view(), name='phone_login'),
    path('verify/', OTPVerificationView.as_view(), name='verify_otp'),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='user_profile'),
]