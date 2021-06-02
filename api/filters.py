import django_filters

from .models import Genre, Title, Category


class CategoryFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(
        field_name='category__slug',
        to_field_name='slug',
        queryset=Category.objects.all()
    )
    genre = django_filters.ModelMultipleChoiceFilter(
        field_name='genre__slug',
        to_field_name='slug',
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
