"""
For future use

from clickgestion.concepts.models import BaseConcept
from crispy_forms.layout import Column, Field, Row
from clickgestion.concepts.filters import ConceptFilter
import django_filters
from crispy_forms.helper import FormHelper, Layout
from django.utils.translation import gettext_lazy
from django.db.models import Q


class DepositFilter(ConceptFilter):

    returned = django_filters.BooleanFilter(method='returned_filter')
    returned.field.label = gettext_lazy('Returned')

    concept_name = django_filters.ChoiceFilter(
        choices=[
            (x, x) for x in
            BaseConcept.objects.filter(
                accounting_group='Deposits').values_list('concept_name', flat=True).order_by('concept_name').distinct()
        ],
    )
    concept_name.field.label = gettext_lazy('Type')

    @property
    def form(self):
        form = super().form
        form.helper = FormHelper()
        form.helper.form_tag = False

        form.helper.layout = Layout(
            Row(
                Column(
                    Field(
                        'transaction__apt_number',
                    ),
                    css_class='col-2',
                ),
                Column(
                    Field(
                        'transaction__client_first_name',
                    ),
                    css_class='col-5',
                ),
                Column(
                    Field(
                        'transaction__client_last_name',
                    ),
                    css_class='col-5',
                ),
                css_class='justify-content-center',
            ),
            Row(
                Column(
                    Field(
                        'start_date',
                    ),
                    css_class='col-6',
                ),
                Column(
                    Field(
                        'end_date',
                    ),
                    css_class='col-6',
                ),
                css_class='justify-content-center',
            ),
            Row(
                Column(
                    Field(
                        'concept_name',
                    ),
                    css_class='col-4',
                ),
                Column(
                    Field(
                        'returned',
                    ),
                    css_class='col-4',
                ),
                Column(
                    Field(
                        'transaction__employee',
                    ),
                    css_class='col-4',
                ),
                css_class='justify-content-center',
            ),
            Row(
                Column(
                    Field(
                        'code',
                    ),
                    css_class='col-6',
                ),
                Column(
                    Field(
                        'transaction__closed_date',
                    ),
                    css_class='col-6',
                ),
                css_class='justify-content-center',
            ),
        )
        return form

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
            accounting_group='Deposits',
            transaction__closed=True,
        )


"""
