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

from accounts.views import UserFollowersViewSet, AuthViewSet, UserSearchViewSet
from accounts.views import UserFollowersViewSet, AuthViewSet, BlockUserByAdminViewSet

from rest_framework_nested import routers


router = routers.SimpleRouter()
router.register(r'auth', AuthViewSet, basename='register')
router.register(r'page', UserFollowersViewSet, basename='page-followers')
router.register(r'find_user', UserSearchViewSet, basename='user-search')
router.register(r'users', BlockUserByAdminViewSet, basename='block-user')


urlpatterns = [
    path("api/v1/", include(router.urls)),
]
