from rest_framework import serializers

from innoapp.models import Page, Post, Tag


class PageSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Page
        fields = (
            "name", "uuid", "description", "tags", "owner", "followers", "image", "is_private", "follow_requests",
            "unblock_date")


class PostSerializer(serializers.ModelSerializer):
    page = PageSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ("page", "content", "reply_to", "created_at", "updated_at")


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ["name"]