from __future__ import unicode_literals
from django.utils.translation import gettext_lazy
from clickgestion.concepts.models import BaseConcept, ConceptSettings, ConceptValue
from django.db import models


class DepositReturnSettings(ConceptSettings):
    """
    Deposit Return Concept Settings
    """
    class Meta:
        verbose_name = gettext_lazy('Deposit Return Settings')
        verbose_name_plural = gettext_lazy('Deposit Return Settings')


class DepositReturn(BaseConcept):
    """
    Deposit Return
    Return a damage deposit to a client
    """
    # The concept that this one returns
    returned_deposit = models.ForeignKey(
        'concepts.BaseConcept',
        verbose_name=gettext_lazy('Returned Deposit'),
        related_name='deposit_return', on_delete=models.CASCADE,
    )

    #BaseConcept settings
    _url = '/deposit-returns/{}'
    _settings_class = DepositReturnSettings
    _code_initials = 'DR'
    _concept_class = 'depositreturn'
    _verbose_name = 'Deposit Return'

    class Meta:
        verbose_name = gettext_lazy('Deposit Return')
        verbose_name_plural = gettext_lazy('Deposit Returns')

    def __str__(self):
        return self.code

    @property
    def description_short(self):
        desc = '{}: {}'.format(gettext_lazy('Return'), self.returned_deposit.description_short)
        return desc

    def save(self):
        value = ConceptValue(
            amount=self.returned_deposit.value.amount,
            credit=False,
            currency=self.returned_deposit.value.currency,
        )
        value.save()
        self.value = value
        super().save()


