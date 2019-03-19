import django_filters
from django.utils.translation import gettext_lazy
from clickgestion.concepts.models import BaseConcept
from crispy_forms.helper import FormHelper


class ConceptFilter(django_filters.FilterSet):

    code = django_filters.CharFilter(lookup_expr='icontains')
    code.field.label = gettext_lazy('Reference')
    code.field.widget.attrs['placeholder'] = gettext_lazy('Search by reference number')
    code.field.widget.attrs['class'] = 'form-control'
    transaction__closed_date = django_filters.DateFromToRangeFilter()
    transaction__closed_date.field.label = gettext_lazy('Transaction Date Range')
    transaction__closed_date.field.widget.attrs['type'] = 'date'
    transaction__closed_date.field.widget.attrs['class'] = 'dateinput form-control'
    end_date = django_filters.DateFromToRangeFilter()
    end_date.field.label = gettext_lazy('End Date Range')
    end_date.field.widget.attrs['type'] = 'date'
    end_date.field.widget.attrs['class'] = 'dateinput form-control'
    start_date = django_filters.DateFromToRangeFilter()
    start_date.field.label = gettext_lazy('Start Date Range')
    start_date.field.widget.attrs['type'] = 'date'
    start_date.field.widget.attrs['class'] = 'dateinput form-control'

    class Meta:
        model = BaseConcept
        fields = [
            'code',
            'accounting_group',
            'concept_name',
            'transaction__closed_date',
            'start_date',
            'end_date',
        ]

    @property
    def form(self):
        form = super().form
        form.helper = FormHelper()
        form.helper.form_tag = False
        return form
