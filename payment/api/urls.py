
from django.urls import path
from payment.api.views import PaymentVerifyAPIView

app_name = 'payment'

urlpatterns = [
    path('verify/', PaymentVerifyAPIView.as_view(), name='verify-payment'),
]
