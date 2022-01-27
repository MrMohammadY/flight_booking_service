from abc import abstractmethod

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.utils import redis_check_otp
from accounts.validators import phone_number_validation

User = get_user_model()


class OTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=[phone_number_validation])


class UserRegistrationSerializer(serializers.ModelSerializer):
    otp_code = serializers.IntegerField(max_value=9999, min_value=1000, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'password', 'otp_code')
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
        }

    def validate(self, attrs):
        redis_check_otp(attrs.get('phone_number'), attrs.pop('otp_code'))
        return attrs

    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)


class CustomTokenObtainSerializer:
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    @abstractmethod
    def validate(self, attrs):
        refresh = self.get_token(self.user)

        attrs['username'] = self.user.username
        attrs['email'] = self.user.email
        attrs['phone_number'] = self.user.phone_number
        attrs['access'] = str(refresh.access_token)
        attrs['refresh'] = str(refresh)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return attrs


class UserPasswordLoginSerializer(CustomTokenObtainSerializer, serializers.Serializer):
    phone_number = serializers.CharField(validators=[phone_number_validation])
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):

        authenticate_kwargs = {
            'request': self.context['request'],
            'password': attrs.pop('password'),
        }

        try:
            user = User.objects.get(phone_number=attrs['phone_number'])
            authenticate_kwargs['username'] = user.username
        except User.DoesNotExist:
            raise ValidationError(_('phone number or password incorrect!'))
        else:
            if not user.check_password(authenticate_kwargs['password']):
                raise ValidationError(_('phone number or password incorrect!'))

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(self.error_messages['no_active_account'], 'no_active_account', )

        return super().validate(attrs)


class UserOTPLoginSerializer(CustomTokenObtainSerializer, serializers.Serializer):
    phone_number = serializers.CharField(validators=[phone_number_validation])
    code = serializers.IntegerField(write_only=True)

    def validate(self, attrs):
        try:
            user = User.objects.get(phone_number=attrs['phone_number'])
        except User.DoesNotExist:
            raise ValidationError(_('user with this phone number does not exists!'))
        else:
            redis_check_otp(user.phone_number, attrs.pop('code'))
            authenticate_kwargs = dict(request=self.context['request'], username=user.username, password=user.password)

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(self.error_messages['no_active_account'], 'no_active_account', )

        return super().validate(attrs)


class ForgotPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(write_only=True, validators=[phone_number_validation])
    new_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    otp_code = serializers.IntegerField(max_value=9999, min_value=1000, write_only=True)

    def validate(self, attrs):
        try:
            attrs['user'] = User.objects.get(phone_number=attrs['phone_number'])
        except User.DoesNotExist:
            raise ValidationError(_('User whit this phone number not exists!'))

        if attrs['new_password'] != attrs['confirm_password']:
            raise ValidationError(_('password and confirm password not equal!'))
        redis_check_otp(attrs.get('phone_number'), attrs['otp_code'])

        return attrs

    def update(self, instance, validated_data):
        self.instance.password = make_password(validated_data['new_password'])
        self.instance.save()
        return self.instance
