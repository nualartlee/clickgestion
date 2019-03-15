import django_filters
from django.utils.translation import gettext_lazy
from clickgestion.concepts.filters import ConceptFilter
from crispy_forms.helper import FormHelper
from django.db.models import IntegerField, Case, When, Count, Q


class DepositFilter(ConceptFilter):

    returned = django_filters.BooleanFilter(method='returned_filter')
    returned.field.label = gettext_lazy('Returned')

    def returned_filter(self, queryset, name, value):

        # Returned
        if value:
            return queryset.filter(depositreturns__transaction__closed=True)

        # Not returned
        else:
            return queryset.filter(Q(depositreturns__transaction__closed=False) | Q(depositreturns__transaction=None))

    @property
    def qs(self):
        concepts = super().qs
        return concepts.filter(
            concept_class__in=['aptrentaldeposit'],
            transaction__closed=True,
        )


