import django_filters
from django import forms
from .models import Post, Category

class PostFilter(django_filters.FilterSet):
    # Поиск по названию (содержит, без учёта регистра)
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='По названию'
    )
    # Поиск по категориям (можно выбрать несколько)
    categories = django_filters.ModelMultipleChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        label='Категории',
        widget=forms.CheckboxSelectMultiple  # можно и SelectMultiple
    )
    # Дата позже указанной (позже = больше, чем введённая дата)
    created_after = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gt',
        label='Позже даты',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = ['title', 'categories', 'created_after']  # имена полей фильтра