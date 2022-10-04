from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers import UserSerializer
from accounts.generate_token import CustomTokenGenerator
from accounts.services.check_login import CheckLogin


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserFollowersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(follows=self.kwargs['page_pk'])


class UserRequestsViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(requests=self.kwargs['page_pk'])


class RegisterViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(methods=['post'], detail=False)
    def register(self, request):
        return Response({'message': 'success'})


class LoginViewSet(viewsets.ModelViewSet):
    # serializer_class = UserSerializer
    # queryset = User.objects.all()

    @action(methods=['post'], detail=False)
    def login(self, request):
        print("hi")
        CheckLogin.check_login(request)
        response = Response()
        response.headers = {'jwt': CustomTokenGenerator.generate_token(request)}
        return response


class LogoutViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(methods=['post'], detail=False)
    def logout(self, request):
        response = Response()
        response.headers.pop('jwt')
        response.data = {'message': 'success'}
        return response
