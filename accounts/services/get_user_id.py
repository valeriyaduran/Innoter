import jwt
from django.http import HttpResponseForbidden

from innotter import settings


class GetUserId:
    @staticmethod
    def get_user_id(request):
        try:
            user_id = jwt.decode(request.headers['jwt'], settings.SECRET_KEY, algorithms=["HS256"])['user_id']
        except jwt.ExpiredSignatureError:
            return HttpResponseForbidden("Invalid signature or signature has expired")
        return user_id
