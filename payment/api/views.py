from django.shortcuts import redirect
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from payment.api.permissions import PaymentCheck
from basket.models import Cart
from payment.api.serializers import PaymentVerifySerializer
from payment.models import Invoice, Payment


class PaymentVerifyAPIView(UpdateAPIView):
    """
    Get boolean field to change is paid last payment
    """
    permission_classes = (IsAuthenticated, PaymentCheck)
    serializer_class = PaymentVerifySerializer
    queryset = Payment.objects.all()

    def get_object(self):
        cart = Cart.get_or_created_cart(self.request.user)
        try:
            payment = cart.invoice.payments.last()
        except Invoice.DoesNotExist:
            raise ValidationError('invoice does not exists!')
        if not cart.cart_is_empty():
            return redirect('basket:cart-checkout')
        return payment


    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return Response(dict(**response.data, message='Your transaction is submit.', ))
        return response
