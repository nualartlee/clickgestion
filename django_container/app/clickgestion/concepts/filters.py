from django.apps import apps
import django_filters
from django.utils.translation import gettext_lazy
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Column, Field, Row
from django.db.models import Q
from django.conf import settings

BaseConcept = apps.get_model('concepts.baseconcept')


class ConceptFilter(django_filters.FilterSet):

    transaction__apt_number = django_filters.NumberFilter()
    transaction__apt_number.field.label = gettext_lazy('Apt.')
    transaction__apt_number.field.widget.attrs['placeholder'] = '101'

    transaction__client_first_name = django_filters.CharFilter(lookup_expr='icontains')
    transaction__client_first_name.field.label = gettext_lazy('First Name')
    transaction__client_first_name.field.widget.attrs['placeholder'] = 'Joh...'

    transaction__client_last_name = django_filters.CharFilter(lookup_expr='icontains')
    transaction__client_last_name.field.label = gettext_lazy('Last Name')
    transaction__client_last_name.field.widget.attrs['placeholder'] = 'Smi...'

    start_date = django_filters.DateFromToRangeFilter()
    start_date.field.label = ''
    start_date.field.widget.attrs['fromlabel'] = 'Start Date From'
    start_date.field.widget.attrs['tolabel'] = 'To'
    start_date.field.widget.attrs['type'] = 'date'
    start_date.field.widget.attrs['class'] = 'dateinput form-control'
    start_date.field.widget.template_name = 'core/date-from-to-widget.html'

    end_date = django_filters.DateFromToRangeFilter()
    end_date.field.label = ''
    end_date.field.widget.attrs['fromlabel'] = 'End Date From'
    end_date.field.widget.attrs['tolabel'] = 'To'
    end_date.field.widget.attrs['type'] = 'date'
    end_date.field.widget.attrs['class'] = 'dateinput form-control'
    end_date.field.widget.template_name = 'core/date-from-to-widget.html'

    code = django_filters.CharFilter(lookup_expr='icontains')
    code.field.label = gettext_lazy('Reference')
    code.field.widget.attrs['placeholder'] = 'T00...'
    code.field.widget.attrs['class'] = 'form-control'

    transaction__closed_date = django_filters.DateFromToRangeFilter()
    transaction__closed_date.field.label = ''
    transaction__closed_date.field.widget.attrs['fromlabel'] = 'Transactions From'
    transaction__closed_date.field.widget.attrs['tolabel'] = 'To'
    transaction__closed_date.field.widget.attrs['type'] = 'date'
    transaction__closed_date.field.widget.attrs['class'] = 'dateinput form-control'
    transaction__closed_date.field.widget.template_name = 'core/date-from-to-widget.html'

    accounting_group = django_filters.ChoiceFilter(
        choices=[
            (x, x) for x in BaseConcept.objects.values_list(
                'accounting_group', flat=True).order_by('accounting_group').distinct()
        ],
    )

    concept_name = django_filters.ChoiceFilter(
        choices=[
            (x, x) for x in BaseConcept.objects.values_list(
                'concept_name', flat=True).order_by('concept_name').distinct()
        ],
    )
    concept_name.field.label = gettext_lazy('Type')

    deposit_status = django_filters.BooleanFilter(method='deposit_status_filter')
    deposit_status.field.label = gettext_lazy('Deposit Status')
    deposit_status.field.widget.choices = [
        ('1', '---------'),
        ('2', gettext_lazy('Returned')),
        ('3', gettext_lazy('Not Returned'))
    ]

    refund_status = django_filters.BooleanFilter(method='refund_status_filter')
    refund_status.field.label = gettext_lazy('Refund Status')
    refund_status.field.widget.choices = [
        ('1', '---------'),
        ('2', gettext_lazy('Refunded')),
        ('3', gettext_lazy('Not Refunded'))
    ]

    class Meta:
        model = BaseConcept
        fields = [
            'accounting_group',
            'code',
            'concept_name',
            'end_date',
            'start_date',
            'transaction__apt_number',
            'transaction__client_first_name',
            'transaction__client_last_name',
            'transaction__closed_date',
            'transaction__employee',
        ]

    def deposit_status_filter(self, queryset, name, value):

        # Returned = 2 = True
        if value:
            return queryset \
                .filter(concept_class__in=settings.DEPOSIT_CONCEPTS)\
                .filter(depositreturns__transaction__closed=True)

        # Not returned = 3 = False
        else:
            return queryset\
                .filter(concept_class__in=settings.DEPOSIT_CONCEPTS)\
                .filter(Q(depositreturns__transaction__closed=False) | Q(depositreturns__transaction=None))

    @property
    def form(self):
        form = super().form

        # Highlight applied filters
        for field in form.fields:
            for variation in [field, field + '_after', field + '_before']:
                if variation in form.data:
                    if form.data[variation]:
                        if 'class' in form.fields[field].widget.attrs:
                            form.fields[field].widget.attrs['class'] += ' text-success'
                        else:
                            form.fields[field].widget.attrs['class'] = 'text-success'

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
                        'accounting_group',
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
            Row(
                Column(
                    Field(
                        'deposit_status',
                    ),
                    css_class='col-4',
                ),
                Column(
                    Field(
                        'refund_status',
                    ),
                    css_class='col-4',
                ),
            ),
        )
        return form

    def refund_status_filter(self, queryset, name, value):

        # Refunded = 2 = True
        if value:
            return queryset \
                .filter(refunds__transaction__closed=True)

        # Not refunded = 3 = False
        else:
            return queryset \
                .filter(accounting_group='Production') \
                .exclude(concept_name='Refund') \
                .filter(Q(refunds__transaction__closed=False) | Q(refunds__transaction=None))
