import django_filters.rest_framework
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, mixins, permissions

from .filters import TitleFilter
from .models import Genre, Category, Title, Review, Comment
from .permissions import IsOwner, IsAdmin, IsModerator
from .serializers import (GenreSerializer, CategorySerializer,
                          TitleReadSerializer, CommentsSerializer,
                          TitleCreateSerializer, ReviewSerializer)


class CustomViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """It's a basic set for GET, POST, PUT methods"""
    pass


class GenreViewSet(CustomViewSet):
    """
    url host:port/api/v1/genres/
    Available method:
    GET: Any
    POST: Only Admin
    DELETE: Only Admin
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CustomViewSet):
    """
    url host:port/api/v1/categories/
    Available method:
    GET: Any
    POST: Only Admin
    DELETE: Only Admin
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """
    url: host:port/api/v1/titles/{titles_id}/ (title by using title id)
    url: host:port/api/v1/titles/ (all titles)
    Available method:
    GET: Any
    POST: Only Admin
    PATCH: Only Admin
    DELETE: Only Admin
    """
    category = CategorySerializer
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    serializer_class = TitleReadSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAdmin,)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer
        return TitleReadSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    url: host:port/api/v1/titles/{title_id}/reviews/ :
    (reviews by using title id)

    url: host:port/api/v1/titles/{title_id}/reviews/{review_id}/ :
    (review by using review id)

    Available method:
    GET: Any
    POST: Only Admin
    PATCH: Only Admin
    DELETE: Only Admin
    """
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwner | IsAdmin | IsModerator,
    )
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        reviews = Review.objects.filter(title__pk=title.pk).all()
        return reviews

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    """
    url: host:port/api/v1/titles/{title_id}/reviews/{review_id}/comments/
    url: host:port/api/v1/titles/{title_id}/reviews/{review_id}/comments/
    {comment_id}/

    Available method:
    GET: Any
    POST: Only Admin
    PATCH: Only Admin
    DELETE: Only Admin
    """
    serializer_class = CommentsSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwner | IsAdmin | IsModerator,
    )

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        comments = Comment.objects.filter(review=review.pk)
        return comments

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(review=review)
