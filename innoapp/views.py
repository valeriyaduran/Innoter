from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers import UserSerializer
from accounts.services.email_recipients_service import EmailRecipientsService
from accounts.services.user_service import UserService
from innoapp.exceptions.page_exceptions import PageNotFound
from innoapp.exceptions.post_exceptions import PostNotFound
from innoapp import tasks
from innoapp.models import Page, Post, Tag
from innoapp.permissions import IsAdminModeratorOrForbidden, IsAdminModeratorOrDontSeeBlockedContent
from innoapp.serializers import PageSerializer, PostSerializer, TagSerializer


class PageViewSet(viewsets.ModelViewSet):
    serializer_class = PageSerializer
    permission_classes = [IsAdminModeratorOrDontSeeBlockedContent]

    def get_queryset(self):
        if UserService.is_admin_or_moderator(self.request):
            return Page.objects.all()
        else:
            return Page.objects.filter(owner=User.objects.get(pk=UserService.get_user_id(self.request)))

    def perform_create(self, serializer):
        try:
            my_page = Page.objects.get(owner=User.objects.get(pk=UserService.get_user_id(self.request)))
            if my_page:
                raise ValidationError("Page already exists!")
        except ObjectDoesNotExist:
            serializer.save(owner=User.objects.get(pk=UserService.get_user_id(self.request)))

    def perform_update(self, serializer):
        serializer.save(owner=Page.objects.get(pk=int(self.kwargs['pk'])).owner)


class BlockPageByStaffViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminModeratorOrForbidden]

    @action(methods=['put'], detail=False)
    def block_page(self, request):
        page_to_block = UserService.set_unblock_date(request)
        serializer = PageSerializer(page_to_block)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAdminModeratorOrDontSeeBlockedContent]

    def get_queryset(self):
        if UserService.is_admin_or_moderator(self.request):
            return Post.objects.filter(page=self.kwargs['page_pk'])
        else:
            my_page = UserService.get_current_page(self.request)
            if str(my_page.pk) != self.kwargs['page_pk']:
                raise ValidationError("You don't have a permission to see the posts of this page!")
            return Post.objects.filter(page=self.kwargs['page_pk'])

    def perform_create(self, serializer):
        if UserService.is_admin_or_moderator(self.request):
            serializer.save(page=Page.objects.get(pk=self.kwargs['page_pk']))
        else:
            my_page = UserService.get_current_page(self.request)
            if str(my_page.pk) != self.kwargs['page_pk']:
                raise ValidationError("You don't have a permission to create posts for this page!")
            serializer.save(page=Page.objects.get(pk=self.kwargs['page_pk']))
            recipients,  page_owner = EmailRecipientsService.get_email_recipients(self.request)
            page_owner_serializer = UserSerializer(page_owner)
            tasks.send_email.delay(recipients, page_owner_serializer.data)

    def perform_update(self, serializer):
        serializer.save(page=Page.objects.get(pk=self.kwargs['page_pk']))

    def perform_destroy(self, instance):
        if UserService.is_admin_or_moderator(self.request) or str(UserService.get_current_page(
                self.request).pk) == self.kwargs['page_pk']:
            instance.delete()


class PostReplyViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAdminModeratorOrDontSeeBlockedContent]

    def perform_create(self, serializer):
        try:
            page_for_post_reply = Page.objects.get(posts=self.request.data.get("reply_to"))
        except ObjectDoesNotExist:
            raise PageNotFound()
        if UserService.check_page_restrictions(self.request, page_for_post_reply):
            serializer.save(page=page_for_post_reply)
        else:
            raise ValidationError("You don't have a permission to send the reply!")


class PostsWithMyLikesViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAdminModeratorOrDontSeeBlockedContent]

    def get_queryset(self):
        posts = Post.objects.filter(liked_by=UserService.get_user_id(self.request))
        return posts


class PostLikesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminModeratorOrDontSeeBlockedContent]

    @action(methods=['post'], detail=False)
    def like(self, request):
        try:
            user_post = Post.objects.get(pk=request.data.get("post"))
        except ObjectDoesNotExist:
            raise PostNotFound()
        try:
            page_for_post_like = Page.objects.get(posts=user_post)
        except ObjectDoesNotExist:
            raise PageNotFound()
        if UserService.check_page_restrictions(request, page_for_post_like):
            if user_post.liked_by.filter(pk=UserService.get_user_id(request)).exists():
                user_post.liked_by.remove(UserService.get_user_id(request))
            else:
                user_post.liked_by.add(UserService.get_user_id(request))
        else:
            raise ValidationError("You don't have a permission to like the post!")
        serializer = PostSerializer(user_post)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [IsAdminModeratorOrDontSeeBlockedContent]

    def get_queryset(self):
        if UserService.is_admin_or_moderator(self.request):
            return Tag.objects.filter(pages=self.kwargs['page_pk'])
        else:
            my_page = UserService.get_current_page(self.request)
            if str(my_page.pk) != self.kwargs['page_pk']:
                raise ValidationError("You don't have a permission to see the tags of this page!")
            return Tag.objects.filter(pages=self.kwargs['page_pk'])

    def perform_create(self, serializer):
        if UserService.is_admin_or_moderator(self.request):
            serializer.save(pages=Page.objects.filter(pk=self.kwargs['page_pk']))
        else:
            my_page = UserService.get_current_page(self.request)
            if str(my_page.pk) != self.kwargs['page_pk']:
                raise ValidationError("You don't have a permission to create tags for this page!")
            serializer.save(pages=Page.objects.filter(pk=self.kwargs['page_pk']))


class FeedViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        today = datetime.now().date()
        my_posts = Post.objects.filter(page__owner__pk=UserService.get_user_id(self.request)).filter(
            created_at__contains=today)
        followed_pages_posts = Post.objects.filter(page__followers=UserService.get_user_id(self.request)).filter(
            created_at__contains=today).filter(page__owner__is_blocked=False)
        all_posts = my_posts | followed_pages_posts
        return all_posts


class PageSearchViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'uuid', 'tags__name']
