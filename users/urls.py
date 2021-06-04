from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MeViewSet, UserViewSet

v1_router = DefaultRouter()
v1_router.register('', UserViewSet, basename='Users')

urlpatterns = [
    path('me/', MeViewSet.as_view(
        {'get': 'retrieve', 'patch': 'update'}),
        name='Me'),
    path('', include(v1_router.urls)),
]