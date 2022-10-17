"""innotter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from innoapp.views import PageViewSet, PostViewSet, TagViewSet, PostLikesViewSet, PostsWithMyLikesViewSet, \
    PostReplyViewSet, BlockPageByStaffViewSet

from rest_framework_nested import routers

page_router = routers.SimpleRouter()
page_router.register(r'pages', PageViewSet, basename='pages')
post_router = routers.NestedSimpleRouter(page_router, r'pages', lookup='page')
post_router.register(r'posts', PostViewSet, basename='page-posts')
tag_router = routers.NestedSimpleRouter(page_router, r'pages', lookup='page')
tag_router.register(r'tags', TagViewSet, basename='page-tags')
router = routers.SimpleRouter()
router.register(r'post', PostLikesViewSet, basename='post-likes')
router.register(r'posts_with_my_likes', PostsWithMyLikesViewSet, basename='liked-posts')
router.register(r'send_post_reply', PostReplyViewSet, basename='post-reply')
router.register(r'block_page', BlockPageByStaffViewSet, basename='block-page')

urlpatterns = [
    path("api/v1/", include(page_router.urls)),
    path("api/v1/", include(post_router.urls)),
    path("api/v1/", include(tag_router.urls)),
    path("api/v1/", include(router.urls))
]
