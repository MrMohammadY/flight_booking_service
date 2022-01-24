from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.api.serializers import OTPSerializer, UserRegistrationSerializer, UserPasswordLoginSerializer, \
    UserOTPLoginSerializer, ForgotPasswordSerializer
from accounts.utils import redis_set_otp

User = get_user_model()


class SendOTPAPIView(GenericAPIView):
    serializer_class = OTPSerializer

    def get(self, request, *args, **kwargs):
        return Response(self.get_serializer().data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = redis_set_otp(serializer.data['phone_number'])
        return Response(data=dict(status=True, message='We sent OTP code.', OTP_code=code, **serializer.data))


class UserRegistrationAPIView(CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        refresh = RefreshToken.for_user(User.objects.get(username=response.data['username']))
        response.data = dict(**response.data, access=str(refresh.access_token), refresh=str(refresh))
        return response


class UserPasswordLoginAPIView(GenericAPIView):
    lookup_url_kwarg = 'type'

    def get_serializer_class(self):
        if self.kwargs[self.lookup_url_kwarg] == 'otp':
            return UserOTPLoginSerializer
        return UserPasswordLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if self.kwargs[self.lookup_url_kwarg] in ('password', 'otp'):
            return Response(data=serializer.validated_data)
        return Response(
            data=dict(
                message='bad param send, just accept(password, otp). by default we render password login',
                **serializer.validated_data
            )
        )


class ForgotPasswordAPIView(UpdateAPIView):
    serializer_class = ForgotPasswordSerializer

    def get_object(self):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data['user']

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            response.data = {'message': 'password changed successfully.'}
        return response
