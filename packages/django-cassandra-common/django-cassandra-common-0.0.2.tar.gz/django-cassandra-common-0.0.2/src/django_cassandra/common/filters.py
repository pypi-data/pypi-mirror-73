from datetime import timedelta

from django import forms
from django_cassandra_engine.models import DjangoCassandraQuerySet
from django_filters import Filter
from django_filters.constants import EMPTY_VALUES
from django_filters.rest_framework import FilterSet


class FilterSet(FilterSet):
    def filter_queryset(self, queryset):
        for name, value in self.form.cleaned_data.items():
            queryset = self.filters[name].filter(queryset, value)
            assert isinstance(queryset, DjangoCassandraQuerySet), \
                "Expected '%s.%s' to return a DjangoCassandraQuerySet, but got a %s instead." \
                % (type(self).__name__, name, type(queryset).__name__)
        return queryset


class CustomDateTimeFilter(Filter):
    field_class = forms.DateTimeField

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        if self.distinct:
            qs = qs.distinct()
        lookup = '%s__%s' % (self.field_name, self.lookup_expr)
        qs = self.get_method(qs)(**{lookup: value})
        lookup = '%s__%s' % (self.field_name, 'lte')
        qs = self.get_method(qs)(**{lookup: value + timedelta(days=1)})
        return qs
