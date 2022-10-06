from rest_framework import serializers

from accounts.models import User


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

    # def create(self, validated_data):
    #     print("********")
    #     print(self.validated_data)
    #     # print("Hello!!!!")
    #     # user = User(
    #     #     email=validated_data['email'],
    #     #     username=validated_data['username'],
    #     #     image_s3_path=validated_data['image_s3_path'],
    #     #     role=validated_data['role'],
    #     #     is_blocked=validated_data['is_blocked']
    #     # )
    #     # user.set_password(validated_data['password'])
    #     # user.save()
    #     return User.objects.create(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")
        extra_kwargs = {'password': {'write_only': True}}
