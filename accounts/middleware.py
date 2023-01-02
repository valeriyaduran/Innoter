import jwt
from django.http import HttpResponseForbidden
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

from innotter import settings


class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            token = request.headers.get('jwt')
        except Exception:
            raise AuthenticationFailed('Unauthenticated!', status.HTTP_401_UNAUTHORIZED)
        if token:
            try:
                jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            except jwt.DecodeError:
                return HttpResponseForbidden("Invalid signature!")
            except jwt.ExpiredSignatureError:
                return HttpResponseForbidden("Signature has expired!")

        elif request.path not in ('/api/v1/auth/register/', '/api/v1/auth/login/') and not request.path.startswith(
                '/admin/'
        ):
            return HttpResponseForbidden('You are not allowed to perform this action! Please, login before.')
