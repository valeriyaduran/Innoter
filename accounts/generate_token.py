import datetime
import jwt

from accounts.models import User
from innotter import settings


class CustomTokenGenerator:
    @staticmethod
    def generate_token(request):
        user = User.objects.get(email=request.data['email'])

        payload = {
            'user_id': user.pk,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token




