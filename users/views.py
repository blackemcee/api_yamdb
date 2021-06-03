from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from users.models import CustomUser

from .permissions import IsAdminOrDeny
from .serializers import ConfCodeSerializer, UserSerializer


class ConfCodeViewSet (viewsets.ModelViewSet):
    serializer_class = ConfCodeSerializer
    queryset = CustomUser.objects.all()


class UserViewSet (viewsets.ModelViewSet):
    permission_classes = (IsAdminOrDeny, )
    serializer_class = UserSerializer
    filter_backends = (SearchFilter,)
    queryset = CustomUser.objects.all()
    search_fields = ('user__username',)
    lookup_field = 'username'

    def perform_update(self, serializer):
        username = self.kwargs.get('username')
        get_object_or_404(CustomUser, username=username)
        serializer.save()


class MeViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        user = get_object_or_404(CustomUser, pk=request.user.pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        user = get_object_or_404(CustomUser, pk=request.user.pk)
        serializer = UserSerializer(
            instance=user,
            partial=True,
            data=request.data
        )
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)
