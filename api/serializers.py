from django.db.models import Avg
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.validators import UniqueTogetherValidator

from .models import Genre, Category, Title, Review, Comments, User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=False, queryset=User.objects.all(),
        default=CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Review
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
                {"name": genre.name,
                 "slug": genre.slug,
                 } for genre in instance.genre.all()
            ],
            "category": instance.category,
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
        model = Comments
