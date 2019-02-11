from django import forms
from django.utils.translation import gettext
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, Div, Hidden, Layout, Field, Fieldset, Row, Column
from crispy_forms.bootstrap import FieldWithButtons, StrictButton


class TransactionForm(forms.Form):
    client_first_name = forms.CharField(label=gettext('First Name'))
    client_last_name = forms.CharField(label=gettext('Last Name'))
    client_apt_number = forms.CharField(label=gettext('Apartment'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    Field(
                        'client_apt_number',
                        id='client_apt_number',
                        title=gettext("The client's apartment number"),
                        placeholder=gettext("101"),
                        css_class='col-12',
                    ),
                    css_class='col-2',
                ),
                Column(
                    Field(
                        'client_first_name',
                        title=gettext("The client's first name"),
                        placeholder=gettext("John"),
                        css_class='col-12',
                    ),
                    css_class='col-5',
                ),
                Column(
                    Field(
                        'client_last_name',
                        title=gettext("The client's last name"),
                        placeholder=gettext("Smith"),
                        css_class='col-12',
                    ),
                    css_class='col-5',
                ),
            ),
        )


