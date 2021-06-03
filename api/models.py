import django.core.validators as validators
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


class Review(models.Model):
    text = models.TextField(null=False)
    score = models.IntegerField(
        null=False,
        validators=[
            validators.MaxValueValidator(10),
            validators.MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        unique_together = ('author', 'title',)

    def __str__(self):
        return f'Review<id№{self.pk}, {self.text[:15]}>'


class Comments(models.Model):
    """Модель представления комментариев для рецензии"""
    text = models.TextField(null=False)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        null=False,
        related_name='comments'
    )

    def __str__(self):
        return f'Comments <id№{self.pk}, author:{self.review}, {self.text[:15]}>'
