import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from accounts.models import User
from accounts.serializers import UserSerializer
from innotter import settings


class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            token = request.COOKIES.get('jwt')
            if not token:
                raise AuthenticationFailed('Unauthenticated!')
            try:
                decoded_jwt = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Unauthenticated!')
            user = User.objects.filter(decoded_jwt['id']).first()
            serializer = UserSerializer(user)
            return Response(serializer.data)
