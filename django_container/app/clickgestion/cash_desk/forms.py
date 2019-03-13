from django import forms
from django.utils.translation import gettext_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column
from clickgestion.cash_desk.models import CashClose, CashFloatDeposit, CashFloatWithdrawal
from clickgestion.concepts.models import ConceptValue, Currency, get_default_currency


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


class CashFloatDepositForm(forms.ModelForm):

    currency = forms.ModelChoiceField(
        queryset=Currency.objects.filter(enabled=True),
        #initial=get_default_currency(),
        initial=Currency.objects.get(default=True),
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
        #initial=get_default_currency(),
        initial=Currency.objects.get(default=True),
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




