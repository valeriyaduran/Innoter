from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers import UserSerializer
from accounts.generate_token import CustomTokenGenerator


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(follows=self.kwargs['page_pk'])


class UserRequestsViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(requests=self.kwargs['page_pk'])


class RegisterViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer


class LoginViewSet(viewsets.ModelViewSet):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        try:
            user = User.objects.get(email=email)
        except Exception:
            raise AuthenticationFailed('User not found!')

        if user.password != password:
            raise AuthenticationFailed('Incorrect password!')

        response = Response()
        response.headers = {'jwt': CustomTokenGenerator.generate_token(request)}
        return response


class LogoutViewSet(viewsets.ModelViewSet):
    def post(self, request):
        response = Response()
        response.headers.pop('jwt')
        response.data = {'message': 'success'}
        return response
