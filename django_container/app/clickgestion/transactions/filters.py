import django_filters
from django.utils.translation import gettext_lazy
from clickgestion.transactions.models import Transaction
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column


class TransactionFilter(django_filters.FilterSet):

    code = django_filters.CharFilter(lookup_expr='icontains')
    code.field.widget.attrs['placeholder'] = gettext_lazy('Search by code')
    code.field.widget.attrs['class'] = 'form-control'
    closed_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Transaction
        fields = ['code', 'closed_date', 'apt_number', 'client_first_name', 'client_last_name', 'employee',]

    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.helper = FormHelper()
    #    self.helper.form_tag = False
    #    #self.helper.layout = Layout(
    #    #    Row(
    #    #        Column(
    #    #            Field(
    #    #                'checkin',
    #    #                title=gettext_lazy("Arrival date"),
    #    #                css_class='col-8',
    #    #            ),
    #    #            css_class='col-6',
    #    #        ),
    #    #        Column(
    #    #            Field(
    #    #                'checkout',
    #    #                title=gettext_lazy("Departure date"),
    #    #                css_class='col-8',
    #    #            ),
    #    #            css_class='col-6',
    #    #        ),
    #    #    ),
    #    #)

