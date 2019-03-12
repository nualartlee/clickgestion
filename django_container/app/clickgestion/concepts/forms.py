from django import forms
from clickgestion.concepts.models import ConceptValue


class ConceptValueForm(forms.ModelForm):

    class Meta:
        model = ConceptValue
        fields = (
            'currency',
            'amount',
        )


