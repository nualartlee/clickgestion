import django_filters
from django.utils.translation import gettext_lazy
from clickgestion.transactions.models import Transaction
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Column, Field, Row


class TransactionFilter(django_filters.FilterSet):

    apt_number = django_filters.NumberFilter()
    apt_number.field.label = gettext_lazy('Apt.')
    apt_number.field.widget.attrs['placeholder'] = '101'

    code = django_filters.CharFilter(lookup_expr='icontains')
    code.field.label = gettext_lazy('Reference')
    code.field.widget.attrs['placeholder'] = 'T00...'
    code.field.widget.attrs['class'] = 'form-control'

    client_first_name = django_filters.CharFilter(lookup_expr='icontains')
    client_first_name.field.label = gettext_lazy('First Name')
    client_first_name.field.widget.attrs['placeholder'] = 'Joh...'

    client_last_name = django_filters.CharFilter(lookup_expr='icontains')
    client_last_name.field.label = gettext_lazy('Last Name')
    client_last_name.field.widget.attrs['placeholder'] = 'Smi...'

    closed_date = django_filters.DateFromToRangeFilter()
    closed_date.field.label = ''
    closed_date.field.widget.attrs['type'] = 'date'
    closed_date.field.widget.attrs['class'] = 'dateinput form-control'
    closed_date.field.widget.attrs['fromlabel'] = 'From'
    closed_date.field.widget.attrs['tolabel'] = 'To'
    closed_date.field.widget.template_name = 'core/date-from-to-widget.html'

    class Meta:
        model = Transaction
        fields = ['code', 'closed', 'closed_date', 'apt_number', 'client_first_name', 'client_last_name', 'employee',]

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
                        'apt_number',
                    ),
                    css_class='col-2',
                ),
                Column(
                    Field(
                        'client_first_name',
                    ),
                    css_class='col-5',
                ),
                Column(
                    Field(
                        'client_last_name',
                    ),
                    css_class='col-5',
                ),
                css_class='justify-content-center',
            ),
            Row(
                Column(
                    Field(
                        'code',
                    ),
                    css_class='col-3',
                ),
                Column(
                    Field(
                        'closed_date',
                    ),
                    css_class='col-6',
                ),
                Column(
                    Field(
                        'employee',
                    ),
                    css_class='col-3',
                ),
                css_class='justify-content-center',
            ),
        )

        return form

