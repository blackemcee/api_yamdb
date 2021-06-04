from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

v1_router = DefaultRouter()
v1_router.register('v1/genres', GenreViewSet, basename='genres')
v1_router.register('v1/categories', CategoryViewSet, basename='categories')
v1_router.register('v1/titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/users/', include('users.urls')),
    path(
        'v1/auth/', include('users.urls')),
    path('', include(v1_router.urls)),
]
