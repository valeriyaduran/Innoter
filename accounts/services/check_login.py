from rest_framework.exceptions import AuthenticationFailed

from accounts.models import User


class CheckLogin:
    @staticmethod
    def check_login(email, password):
        try:
            user = User.objects.get(email=email)
        except Exception:
            raise AuthenticationFailed('User not found!')

        if user.password != password:
            raise AuthenticationFailed('Incorrect password!')


