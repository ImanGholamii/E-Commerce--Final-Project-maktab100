from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


class EmailOrPhoneModelBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, phone=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(Q(username=email) | Q(phone=username))
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None
