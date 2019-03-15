import django_filters
from django.utils.translation import gettext_lazy
from clickgestion.concepts.models import BaseConcept
from crispy_forms.helper import FormHelper
from django.db.models import IntegerField, Case, When, Count, Q

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


class DepositFilter(ConceptFilter):

    returned = django_filters.BooleanFilter(method='returned_filter')
    returned.field.label = gettext_lazy('Returned')

    def returned_filter(self, queryset, name, value):

        # Returned
        if value:
            return queryset.filter(deposit_returns__transaction__closed=True)

        # Not returned
        else:
            return queryset.filter(Q(deposit_returns__transaction__closed=False) | Q(deposit_returns__transaction=None))

    @property
    def qs(self):
        concepts = super().qs
        return concepts.filter(
            concept_class__in=['aptrentaldeposit'],
            transaction__closed=True,
        )


