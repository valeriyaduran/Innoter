from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "password", "image_s3_path", "role", "is_blocked")
        extra_kwargs = {'password': {'write_only': True}}