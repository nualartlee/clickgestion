from django import forms
from django.utils.translation import gettext
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, Submit
from clickgestion.apt_rentals.models import ApartmentRental
from django.core.exceptions import ValidationError
from django.utils.translation import gettext


class RentalForm(forms.ModelForm):
    checkin = forms.DateField(
        label=gettext('Checkin'),
        widget=forms.DateInput(
            attrs={'type': 'date'},
        ),
    )
    checkout = forms.DateField(
        label=gettext('Checkout'),
        widget=forms.DateInput(
            attrs={'type': 'date'},
        ),
    )
    class Meta:
        model = ApartmentRental
        fields = ('checkin', 'checkout')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    Field(
                        'checkin',
                        label=gettext('Checkin'),
                        title=gettext("Arrival date"),
                        css_class='col-8',
                    ),
                    css_class='col-6',
                ),
                Column(
                    Field(
                        'checkout',
                        label=gettext('Checkout'),
                        title=gettext("Departure date"),
                        css_class='col-8',
                    ),
                    css_class='col-6',
                ),
            ),
        )

    def clean(self):

        # Assert that all nightly prices are set
        rates = ApartmentRental(
            checkin=self.cleaned_data.get('checkin'),
            checkout=self.cleaned_data.get('checkout'),
        ).get_rates()
        if 'missing' in rates:
            error = gettext('Missing prices in selected dates')
            raise ValidationError(error)

        return self.cleaned_data






