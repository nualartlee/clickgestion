from __future__ import unicode_literals
from django.apps import apps
from django.contrib.postgres.fields import ArrayField
from clickgestion.transactions.models import BaseConcept, ConceptValue, ConceptSettings
from django.utils.translation import gettext, gettext_lazy
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class NightRateRange(models.Model):
    start_date = models.DateField(verbose_name=gettext_lazy('Start Date'))
    end_date = models.DateField(verbose_name=gettext_lazy('End Date'))
    monday = models.FloatField(verbose_name=gettext_lazy('Monday'))
    tuesday = models.FloatField(verbose_name=gettext_lazy('Tuesday'))
    wednesday = models.FloatField(verbose_name=gettext_lazy('Wednesday'))
    thursday = models.FloatField(verbose_name=gettext_lazy('Thursday'))
    friday = models.FloatField(verbose_name=gettext_lazy('Friday'))
    saturday = models.FloatField(verbose_name=gettext_lazy('Saturday'))
    sunday = models.FloatField(verbose_name=gettext_lazy('Sunday'))
    created = models.DateTimeField(verbose_name=gettext_lazy('Created'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=gettext_lazy('Updated'), auto_now=True)

    class Meta:
        verbose_name = gettext_lazy('Nightly Rate Range')
        verbose_name_plural = gettext_lazy('Nightly Rate Ranges')

    def __str__(self):
        return gettext('Nightly Rate Range %(id)s' % {'id': self.id})


def get_night_rate(date):
    """
    Get the rate  for a given date.
    :param date: Date
    :return: Cost for the night (always assumed to be default currency)
    """
    # Find the last (latest) rate range that the given date falls in
    try:
        rate = NightRateRange.objects.filter(start_date__lte=date, end_date__gte=date).latest('id')
    except NightRateRange.DoesNotExist:
        return 'missing'
    # Get the rate according to the weekday
    weekday = date.isoweekday()
    if weekday == 1:
        return rate.monday
    if weekday == 2:
        return rate.tuesday
    if weekday == 3:
        return rate.wednesday
    if weekday == 4:
        return rate.thursday
    if weekday == 5:
        return rate.friday
    if weekday == 6:
        return rate.saturday
    if weekday == 7:
        return rate.sunday


class AptRentalSettings(ConceptSettings):
    """
    Apartment Rental Concept Settings
    """
    class Meta:
        verbose_name = gettext_lazy('Apartment Rental Settings')
        verbose_name_plural = gettext_lazy('Apartment Rental Settings')


class AptRental(BaseConcept):
    """
    Transaction Concept
    Apartment rental
    """
    # Number of adults
    adults = models.SmallIntegerField(verbose_name=gettext_lazy('Adults'), default=2)
    # Arrival date
    checkin = models.DateField(verbose_name=gettext_lazy('Check In'))
    # Departure date
    checkout = models.DateField(verbose_name=gettext_lazy('Check Out'))
    # Number of children
    children = models.SmallIntegerField(verbose_name=gettext_lazy('Children'), default=0)
    # Ordered list of daily rates
    rates = ArrayField(models.FloatField(), verbose_name=gettext_lazy('Array Of Rates'))

    #BaseConcept settings
    _url = '/apt-rentals/{}'
    _code_initials = 'AR'
    _concept_class = 'aptrental'
    _settings_class = AptRentalSettings
    _verbose_name = 'Apartment Rental'

    class Meta:
        verbose_name = gettext_lazy('Apartment Rental')
        verbose_name_plural = gettext_lazy('Apartment Rentals')

    def __str__(self):
        return self.code

    @property
    def nights(self):
        """
        :return: The total number of nights
        """
        return (self.checkout - self.checkin).days

    @property
    def description_short(self):
        dict = {
            'checkin': self.checkin.strftime('%a, %d %b %Y'),
            'checkout': self.checkout.strftime('%a, %d %b %Y'),
            'adults': self.adults,
            'children': self.children,
        }
        desc = gettext('Apartment Rental: %(checkin)s - %(checkout)s, Adults: %(adults)s, Children: %(children)s') % dict
        return desc

    def get_current_rates(self):
        """
        :return: The list of nightly rates
        """
        nightly_rates = []
        for i in range(self.nights):
            nightly_rates.append(get_night_rate(self.checkin + timezone.timedelta(days=i)))
        return nightly_rates

    def get_value(self):
        """
        :return:ConceptValue: Total price for the stay
        """
        # Rates are recorded on first save only
        if not self.rates:
            self.rates = self.get_current_rates()
        value_model = apps.get_model('transactions.ConceptValue')
        return value_model(amount=sum(self.rates))


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
    # Arrival date
    deposit_date = models.DateField(verbose_name=gettext_lazy('Check In'))
    # Departure date
    return_date = models.DateField(verbose_name=gettext_lazy('Check Out'))
    # Number of children
    children = models.SmallIntegerField(verbose_name=gettext_lazy('Children'), default=0)

    #BaseConcept settings
    _url = '/apt-rentals/deposits/{}'
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
            self.deposit_date = apt_rental.checkin
            self.return_date = apt_rental.checkout
            self.children = apt_rental.children

    def __str__(self):
        return self.code

    @property
    def description_short(self):
        desc = gettext_lazy('Refundable Deposit') + '; '
        desc += gettext_lazy('Adults') + ': {}, '.format(self.adults)
        desc += gettext_lazy('Children') + ': {}, '.format(self.children)
        desc += gettext_lazy('Nights') + ': {}'.format(self.nights)
        return desc

    @property
    def nights(self):
        return (self.return_date - self.deposit_date).days

    def get_value(self):
        """
        :return: ConceptValue: Amount to deposit
        """
        total =  (self.adults * self.settings.per_adult + self.children * self.settings.per_child) * self.nights
        if total > self.settings.max:
            total = self.settings.max
        if total < self.settings.min:
            total = self.settings.min
        value_model = apps.get_model('transactions.ConceptValue')
        return value_model(amount=total)

    def save(self, *args, **kwargs):
        apt_rental = kwargs.pop('apt_rental', None)
        if apt_rental:
            self.adults = apt_rental.adults
            self.deposit_date = apt_rental.checkin
            self.return_date = apt_rental.checkout
            self.children = apt_rental.children
        super().save(*args, **kwargs)


