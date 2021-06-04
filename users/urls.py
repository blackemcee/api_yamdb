from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import MeViewSet, UserViewSet

v1_router = DefaultRouter()
v1_router.register('', UserViewSet, basename='Users')

urlpatterns = [
    path('me/', MeViewSet.as_view(
        {'get': 'retrieve', 'patch': 'update'}),
        name='Me'),
    path('token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'
         ),
    path('', include(v1_router.urls)),
]
