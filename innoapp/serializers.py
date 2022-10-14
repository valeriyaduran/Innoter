from rest_framework import serializers

from innoapp.models import Page, Post, Tag


class PageSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Page
        fields = ("pk",
                  "name", "uuid", "description", "tags", "owner", "followers", "image", "is_private", "follow_requests",
                  "unblock_date")

    def validate(self, attrs):
        if ' ' in attrs['name'] or ' ' in attrs['uuid']:
            raise serializers.ValidationError("Spaces are not allowed in fields!")
        return attrs


class PostSerializer(serializers.ModelSerializer):
    page = PageSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ("pk", "page", "content", "reply_to", "created_at", "updated_at", "liked_by")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["pk", "name"]

    def validate_name(self, name):
        if ' ' in name:
            raise serializers.ValidationError("Spaces are not allowed for tags!")
        return name