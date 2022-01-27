from django.urls import path
from basket.api.views import TicketCreateAPIView, CartCheckoutAPIView

app_name = 'basket'

urlpatterns = [
    path('cart/ticket/add/', TicketCreateAPIView.as_view(), name='cart-ticket-add'),
    path('cart/checkout/', CartCheckoutAPIView.as_view(), name='cart-checkout'),
]
