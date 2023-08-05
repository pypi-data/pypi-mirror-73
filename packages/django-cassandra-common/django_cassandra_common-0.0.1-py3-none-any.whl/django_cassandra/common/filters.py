from django_cassandra_engine.models import DjangoCassandraQuerySet
from django_filters.rest_framework import FilterSet


class FilterSet(FilterSet):
    def filter_queryset(self, queryset):
        for name, value in self.form.cleaned_data.items():
            queryset = self.filters[name].filter(queryset, value)
            assert isinstance(queryset, DjangoCassandraQuerySet), \
                "Expected '%s.%s' to return a DjangoCassandraQuerySet, but got a %s instead." \
                % (type(self).__name__, name, type(queryset).__name__)
        return queryset
