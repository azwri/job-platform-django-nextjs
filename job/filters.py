from django_filters import rest_framework as filters
from .models import Job

class JobFilter(filters.FilterSet):
    min_salary = filters.NumberFilter(field_name="salary", lookup_expr='gte')
    max_salary = filters.NumberFilter(field_name="salary", lookup_expr='lte')
    title = filters.CharFilter(lookup_expr='icontains')
    location = filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Job
        fields = ['min_salary', 'max_salary', 'title', 'location', 'job_type', 'education', 'experience', 'industry']