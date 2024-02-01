from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateTimeFilter
from .models import Post, User
from django.forms import DateInput


class PostFilter(FilterSet):

    search_author = ModelChoiceFilter(
        field_name='author__user',
        queryset=User.objects.all(),
        label='Автор',
        empty_label='Все авторы',
    )

    search_title = CharFilter(
        field_name='heading',
        label='Заголовок',
        lookup_expr='icontains'
    )

    search_time = DateTimeFilter(
         field_name='time_in',
         label='Дата',
         lookup_expr='date__gte',
         widget=DateInput(attrs={'type': 'date'})
    )