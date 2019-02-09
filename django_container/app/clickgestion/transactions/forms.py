from django import forms
from clickgestion.transactions.models import Transaction
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, Div, Hidden, Layout, Field, Fieldset


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = {
            'client_first_name',
            'client_last_name',
            'apt_number',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
