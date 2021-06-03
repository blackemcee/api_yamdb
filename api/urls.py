from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (GenreViewSet, CategoryViewSet, TitleViewSet, ReviewViewSet, CommentsViewSet)

v1_router = DefaultRouter()
v1_router.register(r'^genres', GenreViewSet, basename='genres')
v1_router.register(r'^categories', CategoryViewSet, basename='categories')
v1_router.register(r'^titles', TitleViewSet, basename='titles')
v1_router.register(r'^titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                   CommentsViewSet, basename='comments')

urlpatterns = [
    path('v1/users/', include('users.urls')),
    path('v1/auth/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/', include(v1_router.urls)),
]
