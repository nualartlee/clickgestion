from __future__ import unicode_literals
from django.utils.translation import gettext_lazy
from clickgestion.concepts.models import BaseConcept, ConceptSettings, ConceptValue
from django.db import models
from django.apps import apps


class AptRentalDepositSettings(ConceptSettings):
    """
    Apartment Rental Deposit Settings
    """
    # Maximum deposit amount
    max = models.FloatField(verbose_name=gettext_lazy('Maximum Amount'), default=300)
    # Minimum deposit amount
    min = models.FloatField(verbose_name=gettext_lazy('Minimum Amount'), default=50)
    # Amount per adult/night
    per_adult = models.FloatField(verbose_name=gettext_lazy('Amount Per Adult/Night'), default=10)
    # Amount per child/night
    per_child = models.FloatField(verbose_name=gettext_lazy('Amount Per Child/Night'), default=5)

    class Meta:
        verbose_name = gettext_lazy('Apartment Rental Deposit Settings')
        verbose_name_plural = gettext_lazy('Apartment Rental Deposit Settings')


class AptRentalDeposit(BaseConcept):
    """
    Transaction Concept
    Apartment rental deposit charge
    """
    # Number of adults
    adults = models.SmallIntegerField(verbose_name=gettext_lazy('Adults'), default=2)
    # Number of children
    children = models.SmallIntegerField(verbose_name=gettext_lazy('Children'), default=0)

    # BaseConcept settings
    _url = '/deposits/aptrental/{}'
    _settings_class = AptRentalDepositSettings
    _code_initials = 'ARD'
    _concept_class = 'aptrentaldeposit'
    _verbose_name = 'Apartment Rental Deposit'

    class Meta:
        verbose_name = gettext_lazy('Apartment Rental Deposit')
        verbose_name_plural = gettext_lazy('Apartment Rental Deposits')

    def __init__(self, *args, **kwargs):
        apt_rental = kwargs.pop('apt_rental', None)
        super().__init__(*args, **kwargs)
        if apt_rental:
            self.adults = apt_rental.adults
            self.start_date = apt_rental.start_date
            self.end_date = apt_rental.end_date
            self.children = apt_rental.children

    def __str__(self):
        return self.code

    @property
    def description_short(self):
        data = {
            'start_date': self.start_date.strftime('%a, %d %b %Y'),
            'end_date': self.end_date.strftime('%a, %d %b %Y'),
            'adults': self.adults,
            'children': self.children,
        }
        desc = gettext_lazy('Apartment Deposit: %(start_date)s - %(end_date)s, Adults: %(adults)s, Children: %(children)s')
        return desc % data

    @property
    def nights(self):
        return (self.end_date - self.start_date).days

    def get_value(self):
        """
        :return: ConceptValue: Amount to deposit
        """
        total = (self.adults * self.settings.per_adult + self.children * self.settings.per_child) * self.nights
        if total > self.settings.max:
            total = self.settings.max
        if total < self.settings.min:
            total = self.settings.min
        value_model = apps.get_model('concepts.ConceptValue')
        return value_model(amount=total)

    def save(self, *args, **kwargs):
        apt_rental = kwargs.pop('apt_rental', None)
        if apt_rental:
            self.adults = apt_rental.adults
            self.start_date = apt_rental.start_date
            self.end_date = apt_rental.end_date
            self.children = apt_rental.children
        super().save(*args, **kwargs)


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
        related_name='depositreturns', on_delete=models.CASCADE,
    )

    # BaseConcept settings
    _url = '/deposits/returns/{}'
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
        desc = '{} {}'.format(gettext_lazy('Return'), self.returned_deposit.description_short)
        return desc

    def save(self, *args, **kwargs):
        value = ConceptValue(
            amount=self.returned_deposit.value.amount,
            credit=False,
            currency=self.returned_deposit.value.currency,
        )
        value.save()
        self.value = value
        super().save(*args, **kwargs)


