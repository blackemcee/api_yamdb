import django_filters.rest_framework
from django.http.request import QueryDict, MultiValueDict
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters, mixins, permissions
from rest_framework.response import Response

from .filters import TitleFilter
from .models import Genre, Category, Title, Review, Comments
from .permissions import IsUser, IsAdminOrModeratorAndReadOnly, ReadOnly
from .serializers import (GenreSerializer, CategorySerializer,
                          TitleReadSerializer, CommentsSerializer, TitleCreateSerializer,
                          ReviewSerializer)


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
    lookup_field = 'slug'


# TODO добавить пермишшены
class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


# TODO добавить пермишшены
class TitleViewSet(viewsets.ModelViewSet):
    category = CategorySerializer
    queryset = Title.objects.all()
    serializer_class = TitleReadSerializer
    permission_classes = (ReadOnly,)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer
        return TitleReadSerializer


# TODO добавить пермишшены
class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminOrModeratorAndReadOnly)
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        reviews = Review.objects.filter(title__pk=title.pk).all()
        return reviews

    def create(self, request, *args, **kwargs):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        dictionary = dict(request.data)
        dictionary.update({'title': [title.pk]})
        qdict = QueryDict('', mutable=True)
        qdict.update(MultiValueDict(dictionary))

        serializer = self.get_serializer(data=qdict)

        result = serializer.is_valid(raise_exception=True)
        if result is False:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# TODO добавить пермишшены
class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsUser,
                          # IsAdmin,
                          # IsModerator,
                          )

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        comments = Comments.objects.filter(review=review.pk)
        return comments

    def create(self, request, *args, **kwargs):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        dictionary = dict(request.data)
        dictionary.update({'title': [title.pk]})
        dictionary.update({'review': [review.pk]})
        qdict = QueryDict('', mutable=True)
        qdict.update(MultiValueDict(dictionary))

        serializer = self.get_serializer(data=qdict)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers)
