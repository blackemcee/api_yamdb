from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.validators import UniqueTogetherValidator

from .models import Genre, Category, Title, Review, Comments, User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=False, queryset=User.objects.all(),
        default=CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Review
        extra_kwargs = {
            'text': {'required': True},
            'score': {'required': True},
        }
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title']
            )
        ]


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=False, queryset=User.objects.all(),
        default=CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Comments
        extra_kwargs = {
            'text': {'required': True},
        }
