from django import forms
from django.utils.translation import gettext
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column
from clickgestion.transactions.models import Transaction


class TransactionEditForm(forms.ModelForm):
    # Pay the transaction if submitted as True
    pay_button = forms.BooleanField(
        initial=False,
        required=False,
    )
    # Save the transaction if submitted as True
    save_button = forms.BooleanField(
        initial=False,
        required=False,
    )
    # Delete the transaction if submitted as True
    cancel_button = forms.BooleanField(
        initial=False,
        required=False,
    )

    class Meta:
        model = Transaction
        fields = (
            'apt_number',
            'client_first_name',
            'client_last_name',
        )
        labels = {
            'apt_number': gettext('Apartment'),
            'client_first_name': gettext('First Name'),
            'client_last_name': gettext('Last Name'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('pay_button', type='hidden'),
            Field('save_button', type='hidden'),
            Field('cancel_button', type='hidden'),
        )

    def is_valid(self):
        """
        Custom form validation.
        """
        valid = super().is_valid()
        # Should have at least one concept
        return valid


class TransactionPayForm(forms.ModelForm):
    # Confirm the transaction if submitted as True
    confirm_button = forms.BooleanField(
        initial=False,
        required=False,
    )
    # Save the transaction if submitted as True
    save_button = forms.BooleanField(
        initial=False,
        required=False,
    )
    # Delete the transaction if submitted as True
    cancel_button = forms.BooleanField(
        initial=False,
        required=False,
    )

    class Meta:
        model = Transaction
        fields = (
            'apt_number',
            'client_first_name',
            'client_last_name',
        )
        labels = {
            'apt_number': gettext('Apartment'),
            'client_first_name': gettext('First Name'),
            'client_last_name': gettext('Last Name'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('confirm_button', type='hidden'),
            Field('save_button', type='hidden'),
            Field('cancel_button', type='hidden'),
            Row(
                Column(
                    Field(
                        'apt_number',
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


