import django_filters
from django.utils.translation import gettext
from clickgestion.transactions.models import Transaction


class EmployeeFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='icontains')
    name.field.widget.attrs['placeholder'] = gettext('Search by employee')
    name.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Transaction
        fields = ['employee',]

