import os
from os.path import join

from dotenv import load_dotenv
from rest_framework.exceptions import AuthenticationFailed
import datetime
import jwt

from accounts.models import User
from innotter import settings
from innotter.settings import BASE_DIR


class AuthService:
    @staticmethod
    def check_login(email, password):
        try:
            user = User.objects.get(email=email)
        except Exception:
            raise AuthenticationFailed('User not found!')

        if user.password != password:
            raise AuthenticationFailed('Incorrect password!')

    @staticmethod
    def generate_token(request):
        dotenv_path = join(BASE_DIR, '.env.dev')
        load_dotenv(dotenv_path)
        minutes_token_valid = os.getenv("MINUTES_TOKEN_VALID")
        user = User.objects.get(email=request.data.get('email'))

        payload = {
            'user_id': user.pk,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=int(minutes_token_valid)),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token
