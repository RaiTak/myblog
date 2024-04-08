from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend


class MyEmailAuthBackend(BaseBackend):
    """
    Аутентифицировать посредством адреса электронной почты.
    """

    def authenticate(self, request, username=None, password=None):
        try:
            user = get_user_model().objects.get(email=username)
            if user.check_password(password):
                return user
        except (get_user_model().DoesNotExist, get_user_model().MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
