from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.response import Response

from accounts.generate_token import CustomTokenGenerator
from accounts.models import User


class CheckLogin:
    @staticmethod
    def check_login(request):
        email = request.data['email']
        password = request.data['password']
        try:
            user = User.objects.get(email=email)
        except Exception:
            raise AuthenticationFailed('User not found!')

        if user.password != password:
            raise AuthenticationFailed('Incorrect password!')

