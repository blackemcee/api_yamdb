import django_filters.rest_framework
from rest_framework import viewsets, filters, mixins, permissions

from .permissions import IsAdminOrDeny, IsUser, IsModerator, ReadOnly
from .filters import CategoryFilter
from .models import Genre, Category, Title
from .serializers import GenreSerializer, CategorySerializer, TitleSerializer


class CustomViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    pass


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    category = CategorySerializer
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsUser,
                          IsModerator)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = CategoryFilter
