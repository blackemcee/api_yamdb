from django.db.models import Avg
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.validators import UniqueTogetherValidator

from .models import Genre, Category, Title, Review, Comments, User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Category


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=False, queryset=User.objects.all(),
        default=CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Review
        extra_kwargs = {'title': {'write_only': True}}

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title']
            )
        ]


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',)
        model = Title

    def to_representation(self, instance):
        reviews = Review.objects.filter(title=instance.id)
        rating = reviews.all().aggregate(Avg('score'))['score__avg']
        return {
            "id": instance.pk,
            "name": instance.name,
            "year": instance.year,
            "rating": rating,
            "description": instance.description,
            "genre": [
                {
                    "name": genre.name,
                    "slug": genre.slug,
                } for genre in instance.genre.all()
            ],
            "category": {
                "name": instance.category.name if instance.category else None,
                "slug": instance.category.slug if instance.category else None,
            },
        }


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=False,
        queryset=User.objects.all(),
        default=CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        # fields = ('id', 'text', 'author', 'pub_date',)
        extra_kwargs = {'review': {'write_only': True}}
        model = Comments
