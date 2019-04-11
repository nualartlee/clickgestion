from __future__ import unicode_literals
from django.apps import apps
from clickgestion.concepts.models import BaseConcept, ConceptSettings, ConceptValue
from django.core.exceptions import FieldError
from django.utils.translation import gettext_lazy
from django.db import models


class AptRentalDepositSettings(ConceptSettings):
    """
    Apartment Rental Deposit Settings
    """
    # Maximum deposit amount
    max = models.DecimalField(verbose_name=gettext_lazy('Maximum Amount'), default=300, decimal_places=2, max_digits=12)
    # Minimum deposit amount
    min = models.DecimalField(verbose_name=gettext_lazy('Minimum Amount'), default=50, decimal_places=2, max_digits=12)
    # Amount per adult/night
    per_adult = models.DecimalField(verbose_name=gettext_lazy('Amount Per Adult/Night'),
                                    default=10, decimal_places=2, max_digits=12)
    # Amount per child/night
    per_child = models.DecimalField(verbose_name=gettext_lazy('Amount Per Child/Night'),
                                    default=5, decimal_places=2, max_digits=12)

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
        aptrental = kwargs.pop('aptrental', None)
        super().__init__(*args, **kwargs)
        if aptrental:
            self.adults = aptrental.adults
            self.start_date = aptrental.start_date
            self.end_date = aptrental.end_date
            self.children = aptrental.children
            if not aptrental.transaction.closed:
                self.transaction = aptrental.transaction

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
    def name(self):
        return self._meta.verbose_name

    @property
    def nights(self):
        return (self.end_date - self.start_date).days

    def get_value(self):
        """
        :return: ConceptValue: Amount to deposit
        """
        # Return the saved value if the transaction is closed
        if self.transaction.closed:
            return self.value
        # Get the current value
        total = (self.adults * self.settings.per_adult + self.children * self.settings.per_child) * self.nights
        if total > self.settings.max:
            total = self.settings.max
        if total < self.settings.min:
            total = self.settings.min
        value_model = apps.get_model('concepts.ConceptValue')
        try:
            self.value.amount = total
        except value_model.DoesNotExist:
            self.value = value_model(amount=total)
        return self.value

    def save(self, *args, **kwargs):
        aptrental = kwargs.pop('aptrental', None)
        if aptrental:
            self.adults = aptrental.adults
            self.start_date = aptrental.start_date
            self.end_date = aptrental.end_date
            self.children = aptrental.children
            if not aptrental.transaction.closed:
                self.transaction = aptrental.transaction
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

    def get_value(self):

        value_model = apps.get_model('concepts.ConceptValue')
        try:
            return self.value
        except value_model.DoesNotExist:
            self.value = ConceptValue(
                amount=self.returned_deposit.value.amount,
                credit=False,
                currency=self.returned_deposit.value.currency,
            )
            self.value.save()
        return self.value

    @property
    def name(self):
        return self._meta.verbose_name

    def save(self, *args, **kwargs):
        if not self.returned_deposit.can_return_deposit:
            raise FieldError('returned_deposit is not returnable')
        super().save(*args, **kwargs)


class ParkingRentalDepositSettings(ConceptSettings):
    """
    Parking Rental Deposit Settings
    """
    # Amount
    amount = models.DecimalField(verbose_name=gettext_lazy('Amount'), default=10, decimal_places=2, max_digits=12)

    class Meta:
        verbose_name = gettext_lazy('Parking Rental Deposit Settings')
        verbose_name_plural = gettext_lazy('Parking Rental Deposit Settings')


class ParkingRentalDeposit(BaseConcept):
    """
    Transaction Concept
    Parking rental deposit
    """
    # Amount
    amount = models.DecimalField(verbose_name=gettext_lazy('Amount'), default=10, decimal_places=2, max_digits=12)

    # BaseConcept settings
    _url = '/deposits/parkingrental/{}'
    _settings_class = ParkingRentalDepositSettings
    _code_initials = 'PRD'
    _concept_class = 'parkingrentaldeposit'
    _verbose_name = 'Parking Rental Deposit'

    class Meta:
        verbose_name = gettext_lazy('Parking Rental Deposit')
        verbose_name_plural = gettext_lazy('Parking Rental Deposits')

    def __init__(self, *args, **kwargs):
        parkingrental = kwargs.pop('parkingrental', None)
        super().__init__(*args, **kwargs)
        if parkingrental:
            self.start_date = parkingrental.start_date
            self.end_date = parkingrental.end_date
            if not parkingrental.transaction.closed:
                self.transaction = parkingrental.transaction

    def __str__(self):
        return self.code

    @property
    def description_short(self):
        return self.name

    @property
    def name(self):
        return self._meta.verbose_name

    def get_value(self):
        """
        :return: ConceptValue: Amount to deposit
        """
        # Return the saved value if the transaction is closed
        if self.transaction.closed:
            return self.value
        # Get the current value
        value_model = apps.get_model('concepts.ConceptValue')
        try:
            self.value.amount = self.settings.amount
        except value_model.DoesNotExist:
            self.value = value_model(amount=self.settings.amount)
        return self.value

    def save(self, *args, **kwargs):
        parkingrental = kwargs.pop('parkingrental', None)
        if parkingrental:
            self.start_date = parkingrental.start_date
            self.end_date = parkingrental.end_date
            if not parkingrental.transaction.closed:
                self.transaction = parkingrental.transaction
        super().save(*args, **kwargs)


class SafeRentalDepositSettings(ConceptSettings):
    """
    Safe Rental Deposit Settings
    """
    # Amount
    amount = models.DecimalField(verbose_name=gettext_lazy('Amount'), default=10, decimal_places=2, max_digits=12)

    class Meta:
        verbose_name = gettext_lazy('Safe Rental Deposit Settings')
        verbose_name_plural = gettext_lazy('Safe Rental Deposit Settings')


class SafeRentalDeposit(BaseConcept):
    """
    Transaction Concept
    Safe rental deposit
    """
    # Amount
    amount = models.DecimalField(verbose_name=gettext_lazy('Amount'), default=10, decimal_places=2, max_digits=12)

    # BaseConcept settings
    _url = '/deposits/saferental/{}'
    _settings_class = SafeRentalDepositSettings
    _code_initials = 'SRD'
    _concept_class = 'saferentaldeposit'
    _verbose_name = 'Safe Rental Deposit'

    class Meta:
        verbose_name = gettext_lazy('Safe Rental Deposit')
        verbose_name_plural = gettext_lazy('Safe Rental Deposits')

    def __init__(self, *args, **kwargs):
        saferental = kwargs.pop('saferental', None)
        super().__init__(*args, **kwargs)
        if saferental:
            self.start_date = saferental.start_date
            self.end_date = saferental.end_date
            if not saferental.transaction.closed:
                self.transaction = saferental.transaction

    def __str__(self):
        return self.code

    @property
    def description_short(self):
        return self.name

    @property
    def name(self):
        return self._meta.verbose_name

    def get_value(self):
        """
        :return: ConceptValue: Amount to deposit
        """
        # Return the saved value if the transaction is closed
        if self.transaction.closed:
            return self.value
        # Get the current value
        value_model = apps.get_model('concepts.ConceptValue')
        try:
            self.value.amount = self.settings.amount
        except value_model.DoesNotExist:
            self.value = value_model(amount=self.settings.amount)
        return self.value

    def save(self, *args, **kwargs):
        saferental = kwargs.pop('saferental', None)
        if saferental:
            self.start_date = saferental.start_date
            self.end_date = saferental.end_date
            if not saferental.transaction.closed:
                self.transaction = saferental.transaction
        super().save(*args, **kwargs)
