import django_filters
from django.utils.translation import gettext_lazy
from clickgestion.transactions.models import Transaction
from crispy_forms.helper import FormHelper


class TransactionFilter(django_filters.FilterSet):

    code = django_filters.CharFilter(lookup_expr='icontains')
    code.field.label = gettext_lazy('Reference')
    code.field.widget.attrs['placeholder'] = gettext_lazy('Search by reference number')
    code.field.widget.attrs['class'] = 'form-control'
    closed_date = django_filters.DateFromToRangeFilter()
    closed_date.field.label = gettext_lazy('Date Range')
    closed_date.field.widget.attrs['type'] = 'date'
    closed_date.field.widget.attrs['class'] = 'dateinput form-control'

    class Meta:
        model = Transaction
        fields = ['code', 'closed', 'closed_date', 'apt_number', 'client_first_name', 'client_last_name', 'employee',]

    @property
    def form(self):
        form = super().form
        form.helper = FormHelper()
        form.helper.form_tag = False
        return form

