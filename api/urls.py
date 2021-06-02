from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GenreViewSet, CategoryViewSet, TitleViewSet

v1_router = DefaultRouter()
v1_router.register('v1/genres', GenreViewSet, basename='genres')
v1_router.register('v1/categories', CategoryViewSet, basename='categories')
v1_router.register('v1/titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('', include(v1_router.urls)),
]
