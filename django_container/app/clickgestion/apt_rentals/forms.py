from django import forms
from django.utils.translation import gettext_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, Submit
from clickgestion.apt_rentals.models import AptRental
from django.core.exceptions import ValidationError


class RentalForm(forms.ModelForm):
    checkin = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'},
        ),
    )
    checkout = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'},
        ),
    )

    class Meta:
        model = AptRental
        fields = ('adults', 'checkin', 'checkout', 'children')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    Field(
                        'checkin',
                        title=gettext_lazy("Arrival date"),
                        css_class='col-8',
                    ),
                    css_class='col-6',
                ),
                Column(
                    Field(
                        'checkout',
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
        )

    def clean(self):

        # Assert that all nightly prices are set
        rates = AptRental(
            checkin=self.cleaned_data.get('checkin'),
            checkout=self.cleaned_data.get('checkout'),
        ).get_current_rates()
        if 'missing' in rates:
            error = gettext_lazy('Missing prices in selected dates')
            raise ValidationError(error)

        return self.cleaned_data






