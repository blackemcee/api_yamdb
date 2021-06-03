from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            )

from .views import GenreViewSet, CategoryViewSet, TitleViewSet

v1_router = DefaultRouter()
v1_router.register('v1/genres', GenreViewSet, basename='genres')
v1_router.register('v1/categories', CategoryViewSet, basename='categories')
v1_router.register('v1/titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/users/', include('users.urls')),
    path(
        'v1/auth/token/', TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path('', include(v1_router.urls)),
]
