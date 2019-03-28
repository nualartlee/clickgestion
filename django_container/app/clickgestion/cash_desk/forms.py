from django.apps import apps
from clickgestion.concepts.forms import ConceptForm
from django import forms
from django.utils.translation import gettext_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Row, Column
from clickgestion.cash_desk.models import CashClose, CashFloatDeposit, CashFloatWithdrawal
from django.core.exceptions import ObjectDoesNotExist, ValidationError


class CashCloseForm(forms.ModelForm):

    class Meta:
        model = CashClose
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    Field(
                        'notes',
                        title=gettext_lazy("Additional notes"),
                        placeholder=gettext_lazy("Add a note..."),
                        css_class='col-12',
                        rows='3',
                    ),
                    css_class='col-12',
                ),

            ),
        )


class CashFloatDepositForm(ConceptForm):

    currency = forms.ModelChoiceField(
        queryset=apps.get_model('concepts.Currency').objects.filter(enabled=True),
        #initial=apps.get_model('concepts.Currency').objects.filter(default=True).first(),
    )
    amount = forms.DecimalField(decimal_places=2)

    class Meta:
        model = CashFloatDeposit
        fields = ('currency', 'amount')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['currency'].initial = apps.get_model('concepts.Currency').objects.filter(default=True).first()
        if self.instance:
            try:
                self.fields['currency'].initial = self.instance.value.currency
                self.fields['amount'].initial = self.instance.value.amount
            except ObjectDoesNotExist:
                pass
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('currency'),
                    css_class='col-2',
                ),
                Column(
                    Field('amount'),
                    css_class='col-2',
                ),
            ),
        )

    def clean_amount(self):
        # Assert that amount is positive
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            error = gettext_lazy('Enter a positive amount.')
            raise ValidationError(error)
        return amount

    def save(self, commit=True):
        value = apps.get_model('concepts.ConceptValue')()
        value.amount = self.cleaned_data['amount']
        value.currency = self.cleaned_data['currency']
        value.save()
        deposit = super().save(commit=False)
        deposit.value = value
        if commit:
            deposit.save()
        return deposit


class CashFloatWithdrawalForm(ConceptForm):

    currency = forms.ModelChoiceField(
        queryset=apps.get_model('concepts.Currency').objects.filter(enabled=True),
        #initial=apps.get_model('concepts.Currency').objects.filter(default=True).first(),
    )
    amount = forms.DecimalField(decimal_places=2)

    class Meta:
        model = CashFloatWithdrawal
        fields = ('currency', 'amount')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['currency'].initial = apps.get_model('concepts.Currency').objects.filter(default=True).first()
        if self.instance:
            try:
                self.fields['currency'].initial = self.instance.value.currency
                self.fields['amount'].initial = self.instance.value.amount
            except ObjectDoesNotExist:
                pass
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('currency'),
                    css_class='col-2',
                ),
                Column(
                    Field('amount'),
                    css_class='col-2',
                ),
            ),
        )

    def clean_amount(self):
        # Assert that amount is positive
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            error = gettext_lazy('Enter a positive amount.')
            raise ValidationError(error)
        return amount

    def save(self, commit=True):
        value = apps.get_model('concepts.ConceptValue')()
        value.amount = self.cleaned_data['amount']
        value.currency = self.cleaned_data['currency']
        value.credit = False
        value.save()
        withdrawal = super().save(commit=False)
        withdrawal.value = value
        if commit:
            withdrawal.save()
        return withdrawal



