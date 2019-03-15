from __future__ import unicode_literals
from django.apps import apps
from django.contrib.postgres.fields import ArrayField
from clickgestion.concepts.models import BaseConcept, ConceptSettings
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
    # Number of children
    children = models.SmallIntegerField(verbose_name=gettext_lazy('Children'), default=0)
    # Ordered list of daily rates
    rates = ArrayField(models.FloatField(), verbose_name=gettext_lazy('Array Of Rates'))

    # BaseConcept settings
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
        return (self.end_date - self.start_date).days

    @property
    def description_short(self):
        data = {
            'start_date': self.start_date.strftime('%a, %d %b %Y'),
            'end_date': self.end_date.strftime('%a, %d %b %Y'),
            'adults': self.adults,
            'children': self.children,
        }
        desc = gettext('Apartment Rental: %(start_date)s - %(end_date)s, Adults: %(adults)s, Children: %(children)s')
        return desc % data

    def get_current_rates(self):
        """
        :return: The list of nightly rates
        """
        nightly_rates = []
        for i in range(self.nights):
            nightly_rates.append(get_night_rate(self.start_date + timezone.timedelta(days=i)))
        return nightly_rates

    def get_value(self):
        """
        :return:ConceptValue: Total price for the stay
        """
        # Rates are recorded on first save only
        if not self.rates:
            self.rates = self.get_current_rates()
        value_model = apps.get_model('concepts.ConceptValue')
        return value_model(amount=sum(self.rates))
