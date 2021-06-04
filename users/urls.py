from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

from .views import (MeViewSet, UserViewSet, get_confirm_code,
                    get_tokens_for_user)

v1_router = DefaultRouter()
v1_router.register('', UserViewSet, basename='Users')

urlpatterns = [
    path('me/', MeViewSet.as_view(
        {'get': 'retrieve', 'patch': 'update'}),
        name='Me'),
    path(r'token/', csrf_exempt(get_tokens_for_user),
         name='get_tokens_for_user'
         ),
    path(r'email/', csrf_exempt(get_confirm_code),
         name='get_confirm_code'
         ),
    path('', include(v1_router.urls)),
]
