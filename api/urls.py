from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (GenreViewSet, CategoryViewSet, TitleViewSet,
                    ReviewViewSet, CommentsViewSet)

v1_router = DefaultRouter()
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments'
)
v1_router.register(r'^titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
v1_router.register(r'^genres', GenreViewSet, basename='genres')
v1_router.register(r'^categories', CategoryViewSet, basename='categories')
v1_router.register(r'^titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/users/', include('users.urls')),
    path('v1/auth/', include('users.urls')),
    path('v1/', include(v1_router.urls)),
]
