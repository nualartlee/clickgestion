from django import forms
from django.utils.translation import gettext_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column
from clickgestion.transactions.models import Transaction, ConceptValue


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
            'apt_number': gettext_lazy('Apartment'),
            'client_first_name': gettext_lazy('First Name'),
            'client_last_name': gettext_lazy('Last Name'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('pay_button', type='hidden'),
            Field('save_button', type='hidden'),
            Field('cancel_button', type='hidden'),
            Field('apt_number', type='hidden'),
            Field('client_first_name', type='hidden'),
            Field('client_last_name', type='hidden'),
        )

    def clean(self):
        """
        Custom form validation.
        """
        super().clean()
        # Should have at least one concept
        if self.instance.concepts.count() == 0:
            raise forms.ValidationError(gettext_lazy('No concepts'))


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
            'client_address',
            'client_email',
            'client_first_name',
            'client_id',
            'client_last_name',
            'client_phone_number',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_required_fields()
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
                        title=gettext_lazy("The client's apartment number"),
                        placeholder=gettext_lazy("101"),
                        css_class='col-12',
                    ),
                    css_class='col-2',
                ),
                Column(
                    Field(
                        'client_first_name',
                        title=gettext_lazy("The client's first name"),
                        placeholder=gettext_lazy("John"),
                        css_class='col-12',
                    ),
                    css_class='col-5',
                ),
                Column(
                    Field(
                        'client_last_name',
                        title=gettext_lazy("The client's last name"),
                        placeholder=gettext_lazy("Smith"),
                        css_class='col-12',
                    ),
                    css_class='col-5',
                ),
            ),
            Row(
                Column(
                    Field(
                        'client_id',
                        title=gettext_lazy("The client's ID/Passport number"),
                        placeholder="AA99999999",
                        css_class='col-12',
                    ),
                    css_class='col-3',
                ),
                Column(
                    Field(
                        'client_email',
                        title=gettext_lazy("The client's email address"),
                        placeholder="client@gmail.com",
                        css_class='col-12',
                    ),
                    css_class='col-5',
                ),
                Column(
                    Field(
                        'client_phone_number',
                        title=gettext_lazy("The client's phone number"),
                        placeholder="+44 141 546 3333",
                        css_class='col-12',
                    ),
                    css_class='col-4',
                ),
            ),
            Row(
                Column(
                    Field(
                        'client_address',
                        title=gettext_lazy("The client's address"),
                        placeholder="10 First Ave",
                        css_class='col-12',
                        rows='5',
                    ),
                    css_class='col-12',
                ),

            ),
        )

    def set_required_fields(self, *args, **kwargs):
        """
        Sets which form fields are required according to the included concepts
        """
        # Get the transaction object
        transaction = self.instance
        # Iterate over the fields, set as required/visible per settings
        for field in self.fields:
            for concept in transaction.concepts.all():
                self.fields[field].hidden = True
                if getattr(concept.settings, field + '_visible', False):
                    self.fields[field].hidden = False
                if getattr(concept.settings, field + '_required', False):
                    self.fields[field].required = True
                    self.fields[field].hidden = False


class ConceptValueForm(forms.ModelForm):

    class Meta:
        model = ConceptValue
        fields = (
            'currency',
            'amount',
        )


