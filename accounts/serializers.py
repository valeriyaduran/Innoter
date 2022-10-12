from rest_framework import serializers
import re

from accounts.models import User
from innoapp.models import Page


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "password", "image_s3_path", "role", "is_blocked")
        extra_kwargs = {'password': {'write_only': True}}


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "password", "image_s3_path", "role", "is_blocked")
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, email):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not re.search(regex, email):
            raise serializers.ValidationError("Incorrect email! Email format must be like 'xxx@xx.xx'")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email already exists!")
        return email


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")
        extra_kwargs = {'password': {'write_only': True}}


class UserFollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]

    def validate_username(self, username):
        if username in User.objects.all():
            return username
        raise serializers.ValidationError("This user is not registered to send the request!")


class MyFollowersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = ["followers"]


class FollowRequestsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = ["follow_requests"]
