from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (GenreViewSet, CategoryViewSet, TitleViewSet,
                    ReviewViewSet, CommentsViewSet)

v1_router = DefaultRouter()
# TODO docs of routing https://www.django-rest-framework.org/api-guide/routers/
v1_router.register(r'^genres', GenreViewSet, basename='genres')
v1_router.register(r'^categories', CategoryViewSet, basename='categories')
v1_router.register(r'^titles', TitleViewSet, basename='titles')
v1_router.register(r'^titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments'
)

urlpatterns = [
    path('v1/users/', include('users.urls')),
    path('v1/auth/', include('users.urls')),
    path('v1/', include(v1_router.urls)),
]
