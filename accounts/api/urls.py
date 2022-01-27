from django.urls import path

from accounts.api.views import SendOTPAPIView, UserRegistrationAPIView, UserPasswordLoginAPIView, ForgotPasswordAPIView

app_name = 'accounts'
urlpatterns = [
    path('otp/', SendOTPAPIView.as_view(), name='send-otp'),
    path('registration/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('login/<str:type>/', UserPasswordLoginAPIView.as_view(), name='user-login'),
    path('forgot/password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
]
