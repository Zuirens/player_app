from django.contrib.auth.backends import ModelBackend
from .models import FbAuthenUser


class FbPwdlessAuthBackend(ModelBackend):
    """Log in to Django without providing a password.

    """
    def authenticate(self, username=None, pwd=None, **kwargs):
        try:
            return FbAuthenUser.objects.get(username=username)
        except FbAuthenUser.DoesNotExist:
            return None

    def get_user(self, id):
        try:
            return FbAuthenUser.objects.get(pk=id)
        except FbAuthenUser.DoesNotExist:
            return None