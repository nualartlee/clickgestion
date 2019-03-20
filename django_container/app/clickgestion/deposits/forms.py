from django import forms
from crispy_forms.helper import FormHelper
from clickgestion.deposits.models import AptRentalDeposit, DepositReturn


class AptRentalDepositForm(forms.ModelForm):

    class Meta:
        model = AptRentalDeposit
        fields = ('adults', 'children', 'end_date', 'start_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class DepositReturnForm(forms.ModelForm):

    class Meta:
        model = DepositReturn
        fields = '__all__'
