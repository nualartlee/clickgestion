from django.apps import apps
from django import forms
from django.utils.translation import gettext_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column
from clickgestion.parking_rentals.models import ParkingRental
from clickgestion.concepts.forms import ConceptForm
from django.utils import timezone
from django.core.exceptions import ValidationError


class ParkingRentalForm(ConceptForm):
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
        model = ParkingRental
        fields = ('end_date', 'start_date')

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
                        'add_deposit',
                        title=gettext_lazy("Add Parking Deposit"),
                        css_class='col-8',
                    ),
                    css_class='col-6',
                ),
            ),
        )

    def clean(self):

        # Assert that all nightly prices are set
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if not start_date or not end_date:
            return
        rates = ParkingRental(
            start_date=start_date,
            end_date=end_date,
        ).get_current_rates()
        if 'missing' in rates:  # pragma: no cover
            error = gettext_lazy('Missing prices in selected dates.')
            raise ValidationError(error)

        # Assert that departure is after arrival
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if start_date and end_date:
            if start_date == end_date:
                error = gettext_lazy('Departure date is the same as arrival.')
                raise ValidationError(error)
            if start_date > end_date:
                error = gettext_lazy('Departure date is before arrival.')
                raise ValidationError(error)

        return self.cleaned_data

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date < (timezone.now() - timezone.timedelta(days=30)).date():
            error = gettext_lazy('Arrival date is too far back.')
            raise ValidationError(error)
        return start_date

    def save(self, commit=True):
        parkingrental = super().save(commit=False)
        if commit:
            parkingrental.save()
            if self.cleaned_data['add_deposit']:
                deposit = apps.get_model('deposits.parkingrentaldeposit')(parkingrental=parkingrental)
                deposit.save()
        return parkingrental
