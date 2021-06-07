from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, get_confirm_code, get_tokens_for_user

v1_router = DefaultRouter()
v1_router.register('', UserViewSet, basename='users')

urlpatterns = [
    path(r'token/', get_tokens_for_user,
         name='get_tokens_for_user'
         ),
    path(r'email/', get_confirm_code,
         name='get_confirm_code'
         ),
    path('', include(v1_router.urls)),
]
