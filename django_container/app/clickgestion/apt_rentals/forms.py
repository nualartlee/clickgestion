from django import forms
from django.utils.translation import gettext_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column
from clickgestion.apt_rentals.models import AptRental, AptRentalDeposit
from django.core.exceptions import ValidationError


class AptRentalForm(forms.ModelForm):
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

    class Meta:
        model = AptRental
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
        )

    def clean(self):

        # Assert that all nightly prices are set
        rates = AptRental(
            start_date=self.cleaned_data.get('start_date'),
            end_date=self.cleaned_data.get('end_date'),
        ).get_current_rates()
        if 'missing' in rates:
            error = gettext_lazy('Missing prices in selected dates')
            raise ValidationError(error)

        return self.cleaned_data


class AptRentalDepositForm(forms.ModelForm):

    class Meta:
        model = AptRentalDeposit
        fields = ('adults', 'children', 'end_date', 'start_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False





