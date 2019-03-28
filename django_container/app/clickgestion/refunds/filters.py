"""
For future use

import django_filters
from django.utils.translation import gettext_lazy
from clickgestion.concepts.filters import ConceptFilter
from crispy_forms.helper import FormHelper
from django.db.models import Q


class RefundFilter(ConceptFilter):

    @property
    def qs(self):
        concepts = super().qs
        return concepts.filter(
            concept_class__in=['refund'],
            transaction__closed=True,
        )

"""

