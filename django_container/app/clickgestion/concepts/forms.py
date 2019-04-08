from clickgestion.concepts.models import BaseConcept, ConceptValue
from django import forms
from django.utils.translation import gettext_lazy
from django.core.exceptions import ValidationError


class ConceptForm(forms.ModelForm):
    # This flag controls the final submit, set as false to update fields dynamically and reload the form
    final_submit = forms.BooleanField(
        initial=True,
        required=False,
        widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Disable if the transaction is closed
        try:
            if self.instance.transaction.closed:
                for field in self.fields:
                    self.fields[field].disabled = True
        except BaseConcept.transaction.RelatedObjectDoesNotExist:
            pass


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

