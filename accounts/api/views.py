from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.api.permissions import IsAnonymous
from accounts.api.serializers import OTPSerializer, UserRegistrationSerializer, UserPasswordLoginSerializer, \
    UserOTPLoginSerializer, ForgotPasswordSerializer
from accounts.utils import redis_set_otp

User = get_user_model()


class SendOTPAPIView(GenericAPIView):
    """
    Request to this view should as anonymous user
    Get a phone number and set key value as phone number and otp code which otp code expired tine is 3 minutes in
    redis database and return that code to user for register and login.
    - phone number should like 981234567890 is 12 character and start with 98
    """
    permission_classes = (IsAnonymous,)
    serializer_class = OTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = redis_set_otp(serializer.data['phone_number'])
        return Response(data=dict(status=True, message='We sent OTP code.', OTP_code=code, **serializer.data))


class UserRegistrationAPIView(CreateAPIView):
    """
    Request to this view should as anonymous user
    Before request to register you should get otp code and send user information:
    - username
    - email
    - phone number
    - password
    - otp code

    """
    permission_classes = (IsAnonymous,)
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        refresh = RefreshToken.for_user(User.objects.get(username=response.data['username']))
        response.data = dict(**response.data, access=str(refresh.access_token), refresh=str(refresh))
        return response


class UserPasswordLoginAPIView(GenericAPIView):
    """
    Request to this view should as anonymous user
    Get type in url, type can be password to get phone number and password or otp code to get phone number and otp code
    if you choose otp code before that you should get otp code
    """
    permission_classes = (IsAnonymous,)
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
    """
    Request to this view should as anonymous user

    Get user information like:
    - phone number
    - new password
    - confirm password
    - otp code

    and reset your password, but you should before this get otp code
    """
    permission_classes = (IsAnonymous,)
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
