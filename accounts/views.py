from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

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


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
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
        # response.set_cookie(key='jwt', value=CustomTokenGenerator.generate_token(request), httponly=True)
        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.headers.pop('jwt')
        # response.delete_cookie('jwt')
        response.data = {'message': 'success'}
        return response
