import django_filters
from django.utils.translation import gettext_lazy
from clickgestion.cash_desk.models import CashClose
from crispy_forms.helper import FormHelper


class CashCloseFilter(django_filters.FilterSet):

    code = django_filters.CharFilter(lookup_expr='icontains')
    code.field.label = gettext_lazy('Reference')
    code.field.widget.attrs['placeholder'] = gettext_lazy('Search by reference number')
    code.field.widget.attrs['class'] = 'form-control'
    created = django_filters.DateFromToRangeFilter()
    created.field.label = gettext_lazy('Date Range')
    created.field.widget.attrs['type'] = 'date'
    created.field.widget.attrs['class'] = 'dateinput form-control'

    class Meta:
        model = CashClose
        fields = ['code', 'created', 'employee', 'notes']

    @property
    def form(self):
        form = super().form
        form.helper = FormHelper()
        form.helper.form_tag = False
        return form
