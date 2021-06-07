import django.core.validators as validators
from django.contrib.auth import get_user_model
from django.db import models

from .validators import title_year_validator

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        'Category name',
        max_length=100,
    )
    slug = models.SlugField(
        'Category slug',
        max_length=20,
        unique=True,
        db_index=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        'Genre name',
        max_length=100,
    )
    slug = models.SlugField(
        'Genre slug',
        max_length=20,
        unique=True,
        db_index=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Title name',
        max_length=200,
    )
    year = models.IntegerField(
        'Title year',
        null=True,
        blank=True,
        validators=(title_year_validator,)
    )
    description = models.TextField(
        'Title description',
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Title genre',
        null=True,
        blank=True,
        db_index=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Title category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True
    )

    class Meta:
        ordering = ['-year']
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def get_genres(self):  # noqa
        return '\n'.join(Genre.objects.values_list('name', flat=True))

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField('Review text', null=False)
    score = models.IntegerField(
        'Review score',
        null=False,
        validators=[
            validators.MaxValueValidator(10, 'Value score from 1 up to 10'),
            validators.MinValueValidator(1, 'Value score from 1 up to 10')
        ],
    )
    pub_date = models.DateTimeField(
        'Date of publishing',
        auto_now_add=True,
        db_index=True
    )
    author = models.ForeignKey(
        User,
        verbose_name='Review author',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Title',
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('author', 'title',),
                                    name='unique_title')
        ]
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ['-pub_date']

    def __str__(self):
        return f'Review<id№{self.pk}, Title№{self.title}>'


class Comment(models.Model):
    text = models.TextField('Comment text', null=False)
    pub_date = models.DateTimeField(
        'Date of publishing',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        verbose_name='Comment author',
        on_delete=models.CASCADE,
        null=False,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        verbose_name='Review',
        on_delete=models.CASCADE,
        null=False,
        related_name='comments',
        db_index=True
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        ordering = ['-pub_date']

    def __str__(self):
        return (f'Comments <id№{self.pk}, author:{self.review}, '
                f'{self.text[:15]}>')
