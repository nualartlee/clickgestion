from django import forms
from django.utils.translation import gettext_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column, Submit
from clickgestion.cash_float.models import CashFloatDeposit, CashFloatWithdrawal
from django.core.exceptions import ValidationError
from clickgestion.transactions.models import ConceptValue, Currency


class CashFloatDepositForm(forms.ModelForm):

    currency = forms.ModelChoiceField(
        queryset=Currency.objects.filter(enabled=True),
        #initial=Currency.objects.get(default=True),
    )
    amount = forms.DecimalField(decimal_places=2)

    class Meta:
        model = CashFloatDeposit
        fields = ('currency', 'amount')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    def save(self, commit=True):
        value = ConceptValue()
        value.amount = self.cleaned_data['amount']
        value.currency = self.cleaned_data['currency']
        value.save()
        deposit = super().save(commit=False)
        deposit.value = value
        deposit.save()
        return deposit


class CashFloatWithdrawalForm(forms.ModelForm):

    currency = forms.ModelChoiceField(
        queryset=Currency.objects.filter(enabled=True),
        #initial=Currency.objects.get(default=True),
    )
    amount = forms.DecimalField(decimal_places=2)

    class Meta:
        model = CashFloatWithdrawal
        fields = ('currency', 'amount')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    def save(self, commit=True):
        value = ConceptValue()
        value.amount = self.cleaned_data['amount']
        value.currency = self.cleaned_data['currency']
        value.credit = False
        value.save()
        withdrawal = super().save(commit=False)
        withdrawal.value = value
        withdrawal.save()
        return withdrawal





