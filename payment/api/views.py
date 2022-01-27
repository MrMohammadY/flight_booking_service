from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from payment.api.permissions import PaymentCheck
from basket.models import Cart
from payment.api.serializers import PaymentVerifySerializer
from payment.models import Invoice


class PaymentVerifyAPIView(UpdateAPIView):
    permission_classes = (IsAuthenticated, PaymentCheck)
    serializer_class = PaymentVerifySerializer

    def get_object(self):
        cart = Cart.get_or_created_cart(self.request.user)
        try:
            payment = cart.invoice.payments.last()
        except Invoice.DoesNotExist:
            raise ValidationError('invoice does not exists!')
        return payment

    def get(self, request, *args, **kwargs):
        self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return Response(dict(**response.data, message='Your transaction is submit.', ))
        return response
