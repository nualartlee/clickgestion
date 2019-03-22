from __future__ import unicode_literals
from clickgestion.concepts.models import BaseConcept, ConceptSettings, ConceptValue
from django.utils.translation import gettext_lazy
from django.core.exceptions import FieldError
from django.db import models


class RefundSettings(ConceptSettings):
    """
    Refund Concept Settings
    """
    class Meta:
        verbose_name = gettext_lazy('Refund Settings')
        verbose_name_plural = gettext_lazy('Refund Settings')


class Refund(BaseConcept):
    """
    Refund
    Refund a concept to a client
    """
    # The concept that this one refunds
    refunded_concept = models.ForeignKey(
        'concepts.BaseConcept',
        verbose_name=gettext_lazy('Refunded Concept'),
        related_name='refunds', on_delete=models.CASCADE,
    )

    # BaseConcept settings
    _url = '/refunds/{}'
    _settings_class = RefundSettings
    _code_initials = 'R'
    _concept_class = 'refund'
    _verbose_name = 'Refund'

    class Meta:
        verbose_name = gettext_lazy('Refund')
        verbose_name_plural = gettext_lazy('Refunds')

    def __str__(self):
        return self.code

    @property
    def description_short(self):
        desc = '{} {}'.format(gettext_lazy('Refund'), self.refunded_concept.description_short)
        return desc

    @property
    def name(self):
        return self._meta.verbose_name

    def save(self, *args, **kwargs):
        if not self.refunded_concept.can_refund:
            raise FieldError('refunded_concept is not refundable')

        value = ConceptValue(
            amount=self.refunded_concept.value.amount,
            credit=False,
            currency=self.refunded_concept.value.currency,
        )
        value.save()
        self.value = value
        super().save(*args, **kwargs)


