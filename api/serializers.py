from django.db.models import Avg
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import Genre, Category, Title, Review, Comment, User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Genre
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = '__all__'
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


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=False,
        queryset=User.objects.all(),
        default=CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        extra_kwargs = {
            'review': {
                'write_only': True,
                'required': False
            }
        }
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=False,
        queryset=User.objects.all(),
        default=CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Review
        extra_kwargs = {
            'title': {'write_only': True,
                      'required': False}
        }

    def validate_author(self, value):
        if self.context['request'].method == 'POST':
            review = Review.objects.filter(
                title__pk=self.context['view'].kwargs.get('title_id'),
                author=self.context['request'].user
            ).first()
            if review:
                raise serializers.ValidationError(
                    'Author and title must be unique for Review')
        return value
