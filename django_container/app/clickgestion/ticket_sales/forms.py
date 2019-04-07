from django.apps import apps
from django import forms
from django.utils.translation import gettext_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column
from clickgestion.ticket_sales.models import TicketSale
from clickgestion.concepts.forms import ConceptForm
from django.utils import timezone
from django.core.exceptions import ValidationError


class TicketSalesForm(ConceptForm):
    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'},
        ),
    )
    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'},
        ),
    )
    add_deposit = forms.BooleanField(initial=False, required=False)

    class Meta:
        model = TicketSale
        fields = ('adults', 'children', 'end_date', 'start_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    Field(
                        'start_date',
                        title=gettext_lazy("Arrival date"),
                        css_class='col-8',
                    ),
                    css_class='col-6',
                ),
                Column(
                    Field(
                        'end_date',
                        title=gettext_lazy("Departure date"),
                        css_class='col-8',
                    ),
                    css_class='col-6',
                ),
            ),
            Row(
                Column(
                    Field(
                        'adults',
                        title=gettext_lazy("Number of adults"),
                        css_class='col-8',
                    ),
                    css_class='col-6',
                ),
                Column(
                    Field(
                        'children',
                        title=gettext_lazy("Number of children"),
                        css_class='col-8',
                    ),
                    css_class='col-6',
                ),
            ),
            Row(
                Column(
                    Field(
                        'add_deposit',
                        title=gettext_lazy("Add Apartment Deposit"),
                        css_class='col-8',
                    ),
                    css_class='col-6',
                ),
            ),
        )

    def clean(self):

        # Assert number of people
        adults = self.cleaned_data.get('adults')
        children = self.cleaned_data.get('children')
        if adults and children:
            if adults + children == 0:
                error = gettext_lazy('No people')
                raise ValidationError(error)

        return self.cleaned_data

    def clean_adults(self):
        adults = self.cleaned_data.get('adults')
        if adults < 0:
            error = gettext_lazy('Invalid value')
            raise ValidationError(error)
        return adults

    def clean_children(self):
        children = self.cleaned_data.get('children')
        if children < 0:
            error = gettext_lazy('Invalid value')
            raise ValidationError(error)
        return children

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date < (timezone.now() - timezone.timedelta(days=30)).date():
            error = gettext_lazy('Ticket date is too far back.')
            raise ValidationError(error)
        return start_date

    def save(self, commit=True):
        ticketsale = super().save(commit=False)
        if commit:
            ticketsale.save()
        return ticketsale
