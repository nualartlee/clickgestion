from django import forms
from django.utils.translation import gettext
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column


class RentalForm(forms.Form):
    checkin = forms.DateField(label=gettext('Checkin'))
    checkout = forms.DateField(label=gettext('Checkout'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    Field(
                        'checkin',
                        title=gettext("Arrival date"),
                        css_class='col-12',
                    ),
                    css_class='col-6',
                ),
                Column(
                    Field(
                        'checkout',
                        title=gettext("Departure date"),
                        css_class='col-12',
                    ),
                    css_class='col-6',
                ),
            ),
        )


