import django_filters
from .models import Task


class TaskFilter(django_filters.FilterSet):

    status = django_filters.ChoiceFilter(
        choices=Task.Status.choices,
    )

    search = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains'
    )

    class Meta:
        model = Task
        fields = [
            "status",
            "search",
        ]
