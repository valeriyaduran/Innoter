import datetime
import jwt

from innotter import settings


class CustomTokenGenerator:
    @staticmethod
    def generate_token(request):
        payload = {
            'id': request.user.pk,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token


