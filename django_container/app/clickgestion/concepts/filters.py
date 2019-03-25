import django_filters
from django.utils.translation import gettext_lazy
from clickgestion.concepts.models import BaseConcept
from crispy_forms.helper import FormHelper


class ConceptFilter(django_filters.FilterSet):

    code = django_filters.CharFilter(lookup_expr='icontains')
    code.field.label = gettext_lazy('Reference')
    code.field.widget.attrs['placeholder'] = 'T00...'
    code.field.widget.attrs['class'] = 'form-control'

    transaction__closed_date = django_filters.DateFromToRangeFilter()
    transaction__closed_date.field.label = gettext_lazy('Transaction Date')
    transaction__closed_date.field.widget.attrs['fromlabel'] = 'From'
    transaction__closed_date.field.widget.attrs['tolabel'] = 'To'
    transaction__closed_date.field.widget.attrs['type'] = 'date'
    transaction__closed_date.field.widget.attrs['class'] = 'dateinput form-control'
    transaction__closed_date.field.widget.template_name = 'core/date-from-to-widget.html'

    end_date = django_filters.DateFromToRangeFilter()
    end_date.field.label = gettext_lazy('Concept Start Date')
    end_date.field.widget.attrs['fromlabel'] = 'From'
    end_date.field.widget.attrs['tolabel'] = 'To'
    end_date.field.widget.attrs['type'] = 'date'
    end_date.field.widget.attrs['class'] = 'dateinput form-control'
    end_date.field.widget.template_name = 'core/date-from-to-widget.html'

    start_date = django_filters.DateFromToRangeFilter()
    start_date.field.label = gettext_lazy('Concept End Date')
    start_date.field.widget.attrs['fromlabel'] = 'From'
    start_date.field.widget.attrs['tolabel'] = 'To'
    start_date.field.widget.attrs['type'] = 'date'
    start_date.field.widget.attrs['class'] = 'dateinput form-control'
    start_date.field.widget.template_name = 'core/date-from-to-widget.html'

    accounting_group = django_filters.ChoiceFilter(
        choices=[(x, x) for x in BaseConcept.objects.values_list('accounting_group', flat=True).distinct()],
    )

    concept_name = django_filters.ChoiceFilter(
        choices=[(x, x) for x in BaseConcept.objects.values_list('concept_name', flat=True).distinct()],
    )

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
