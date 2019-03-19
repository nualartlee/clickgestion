from clickgestion.concepts.models import ConceptValue
from django import forms
from django.utils.translation import gettext_lazy
from django.core.exceptions import ValidationError


class ConceptValueForm(forms.ModelForm):

    class Meta:
        model = ConceptValue
        fields = (
            'currency',
            'amount',
        )

    def clean_amount(self):
        # Assert that amount is positive
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            error = gettext_lazy('Enter a positive amount.')
            raise ValidationError(error)
        return amount

