from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

v1_router = DefaultRouter()

v1_router.register('', UserViewSet, basename='User')


urlpatterns = [
    path('', include(v1_router.urls)),
]
