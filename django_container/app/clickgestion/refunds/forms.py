from django import forms
from crispy_forms.helper import FormHelper
from clickgestion.refunds.models import Refund


class RefundForm(forms.ModelForm):

    class Meta:
        model = Refund
        fields = '__all__'
