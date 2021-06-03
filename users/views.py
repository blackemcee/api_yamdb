from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from users.models import CustomUser

from .permissions import IsAdminOrDeny
from .serializers import ConfCodeSerializer, UserSerializer


class ConfCodeViewSet (viewsets.ModelViewSet):
    serializer_class = ConfCodeSerializer
    queryset = CustomUser.objects.all()


class UserViewSet (viewsets.ModelViewSet):
    permission_classes = (IsAdminOrDeny, IsAuthenticated)
    serializer_class = UserSerializer
    filter_backends = (SearchFilter,)
    queryset = CustomUser.objects.all()
    search_fields = ('user__username',)
    lookup_field = 'username'

    def perform_update(self, serializer):
        username = self.kwargs.get('username')
        get_object_or_404(CustomUser, username=username)
        serializer.save()
