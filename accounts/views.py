from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers import UserSerializer, UserRegisterSerializer
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


class AuthViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(methods=['post'], detail=False)
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.create(**serializer.validated_data)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def login(self, request):
        # serializer = UserLoginSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # print("****", serializer.is_valid())
        # email = serializer.validated_data['email']
        # print("email:", email)
        # password = serializer.validated_data['password']
        # print("password:",password)
        CheckLogin.check_login(request)
        response = Response()
        response.headers = {'jwt': CustomTokenGenerator.generate_token(request)}
        return response

    @action(methods=['post'], detail=False)
    def logout(self, request):
        response = Response()
        response.headers.pop('jwt')
        response.data = {'message': 'success'}
        return response
