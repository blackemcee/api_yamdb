from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        'Category name',
        max_length=100
    )
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        'Genre name',
        max_length=100
    )
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Title name',
        max_length=200
    )
    year = models.IntegerField(
        'Title year',
        null=True,
        blank=True
    )
    description = models.TextField(
        'Title description',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def get_genres(self):
        return '\n'.join([str(genre) for genre in self.genre.all()])

    def __str__(self):
        return self.name
