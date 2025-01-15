import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    completed = django_filters.BooleanFilter(field_name='completed', lookup_expr='exact', label='Completed')
    due_date = django_filters.DateFilter(field_name='due_date', lookup_expr='exact', label='Due Date')
    
    class Meta:
        model = Task
        fields = ['completed', 'due_date']
