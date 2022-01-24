from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class HashedPasswordAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            return User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
