from django.shortcuts import redirect
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from basket.api.serializers import TickerCreateSerializer
from basket.models import Ticket, Cart
from payment.models import Invoice


class TicketCreateAPIView(CreateAPIView):
    """
    Get flight information like:

    - flight id
    - flight seat id
    - first name
    - last name
    - national name
    - birthday

    and create ticket and add to user basket
    """
    permission_classes = (IsAuthenticated,)
    queryset = Ticket.objects.all()
    serializer_class = TickerCreateSerializer

    def perform_create(self, serializer):
        serializer.save(cart=Cart.get_or_created_cart(self.request.user))

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            response.data = dict(message='your ticket is created')
        return response


class CartCheckoutAPIView(GenericAPIView):
    """
    User request to here for create invoice and payment after that user can go to payment verify
    and change to is paid payment.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        cart = Cart.get_or_created_cart(self.request.user)
        if not cart.cart_is_empty():
            Invoice.create_invoice_payment(self.request.user, cart)
            return redirect('payment:verify-payment')
        return Response({'message': 'your cart is empty!'}, status=status.HTTP_406_NOT_ACCEPTABLE)
