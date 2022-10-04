from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.response import Response

from accounts.generate_token import CustomTokenGenerator
from accounts.models import User


class CheckLogin:
    @staticmethod
    def check_login(request):
        try:
            email = request.get('email')
            password = request.get('password')
        except Exception:
            raise NotFound('Email or password not found')
        try:
            user = User.objects.get(email=email)
        except Exception:
            raise AuthenticationFailed('User not found!')

        if user.password != password:
            raise AuthenticationFailed('Incorrect password!')
        print(email, password)

