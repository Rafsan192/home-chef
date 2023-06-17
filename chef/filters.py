import django_filters

from chef.models import Course


class CourseFilter(django_filters.FilterSet):
    class Meta:
        model = Course
        fields = ['title', 'duration', 'price']