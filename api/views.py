import django_filters.rest_framework
from rest_framework import viewsets, filters, mixins

from .filters import CategoryFilter
from .models import Genre, Category, Title
from .serializers import (GenreSerializer, CategorySerializer, TitleSerializer, CommentsSerializer, ReviewSerializer)


class CustomViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    pass


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    category = CategorySerializer
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = CategoryFilter


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
