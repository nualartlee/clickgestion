from django import forms
from django.utils.translation import gettext
from clickgestion.transactions.models import Transaction
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, Div, Hidden, Layout, Field, Fieldset


class TransactionForm(forms.Form):
    client_first_name = forms.CharField(
        widget=forms.TextInput(),
        label=gettext('First Name'),
    )
    client_last_name = forms.CharField(
        widget=forms.TextInput(),
        label=gettext('Last Name'),
    )
    client_apt_number = forms.CharField(
        widget=forms.TextInput(),
        label=gettext('Apartment Number'),
    )

