import django_filters
from .models import Post, Author
from django import forms
from django_filters import DateFilter


class PostFilter(django_filters.FilterSet):
    # date_time = django_filters.DateFromToRangeFilter(
    #     field_name='date_time',
    #     label="Диапазон дат:",
    #     widget=forms.widgets.MultiWidget(widgets=[forms.DateInput(attrs={'type': 'date'}),
    #                                               forms.DateInput(attrs={'type': 'date'})]))
    datetime_f = django_filters.DateFilter(
        field_name='date_time',
        label="После Даты   ",
        widget=forms.DateInput(attrs={'type': 'date'}), lookup_expr='gte',
    )

    autor_f = django_filters.ModelMultipleChoiceFilter(
        field_name='author__author_name',
        label="Автор",
        queryset=Author.objects.all(),
        conjoined=0  # 0=выделив всех, выдаст всё
    )

    title_f = django_filters.Filter(
        field_name='title',
        label="Поиск по заголовку",
        lookup_expr='icontains',
    )


    # class Meta:
    #     model = Product
    #     fields = {
    #         'name': ['icontains'],
    #     }


