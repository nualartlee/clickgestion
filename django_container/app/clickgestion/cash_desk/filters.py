import django_filters
from django.utils.translation import gettext_lazy
from clickgestion.cash_desk.models import CashClose
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Column, Field, Row


class CashCloseFilter(django_filters.FilterSet):

    code = django_filters.CharFilter(lookup_expr='icontains')
    code.field.label = gettext_lazy('Reference')
    code.field.widget.attrs['placeholder'] = 'CC00...'
    code.field.widget.attrs['class'] = 'form-control'

    created = django_filters.DateFromToRangeFilter()
    created.field.label = ''
    created.field.widget.attrs['type'] = 'date'
    created.field.widget.attrs['class'] = 'dateinput form-control'
    created.field.widget.attrs['fromlabel'] = 'From'
    created.field.widget.attrs['tolabel'] = 'To'
    created.field.widget.template_name = 'core/date-from-to-widget.html'

    notes = django_filters.CharFilter(lookup_expr='icontains')
    notes.field.label = gettext_lazy('Notes')
    notes.field.widget.attrs['placeholder'] = '...'

    class Meta:
        model = CashClose
        fields = ['code', 'created', 'employee', 'notes']

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
                        'code',
                    ),
                    css_class='col-3',
                ),
                Column(
                    Field(
                        'created',
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
            Row(
                Column(
                    Field(
                        'notes',
                    ),
                    css_class='col-6',
                ),
            ),
        )
        return form
