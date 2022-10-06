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
from django.contrib import admin
from django.urls import path, include

from accounts.views import UserFollowersViewSet, UserFollowersViewSet, UserRequestsViewSet, AuthViewSet
from innoapp.views import PageViewSet, PostViewSet, TagViewSet

from rest_framework_nested import routers

page_router = routers.SimpleRouter()
page_router.register(r'pages', PageViewSet)
post_router = routers.NestedSimpleRouter(page_router, r'pages', lookup='page')
post_router.register(r'posts', PostViewSet, basename='page-posts')
tag_router = routers.NestedSimpleRouter(page_router, r'pages', lookup='page')
tag_router.register(r'tags', TagViewSet, basename='page-tags')
follower_router = routers.NestedSimpleRouter(page_router, r'pages', lookup='page')
follower_router.register(r'followers', UserFollowersViewSet, basename='page-followers')
follow_request_router = routers.NestedSimpleRouter(page_router, r'pages', lookup='page')
follow_request_router.register(r'follow_requests', UserRequestsViewSet, basename='page-follow_requests')

router = routers.SimpleRouter()
router.register(r'auth', AuthViewSet, basename='register')


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(page_router.urls)),
    path("api/v1/", include(post_router.urls)),
    path("api/v1/", include(tag_router.urls)),
    path("api/v1/", include(follower_router.urls)),
    path("api/v1/", include(router.urls))
]
