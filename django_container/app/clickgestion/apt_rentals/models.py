from __future__ import unicode_literals
from django.contrib.postgres.fields import ArrayField
from clickgestion.transactions.models import ConceptData,ConceptValue, Currency
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


@python_2_unicode_compatible
class ApartmentRental(ConceptData):
    """
    Transaction Concept
    Apartment rental
    """
    # Arrival date
    checkin = models.DateField(verbose_name=gettext_lazy('Check In'))
    # Departure date
    checkout = models.DateField(verbose_name=gettext_lazy('Check Out'))
    # Ordered list of daily rates
    rates = ArrayField(models.FloatField(), verbose_name=gettext_lazy('Array Of Rates'))

    class Meta:
        verbose_name = gettext_lazy('Apartment Rental')
        verbose_name_plural = gettext_lazy('Apartment Rentals')

    def __str__(self):
        return '{0}-AR{1}'.format(self.transaction.code, self.id)

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
            'nights': self.nights,
            'price': self.price,
        }
        desc = gettext('Apartment Rental: %(checkin)s - %(checkout)s, %(nights)s nights, %(price)s') % dict
        return desc

    @property
    def description_long(self):
        return self.description_short

    def get_rates(self):
        """
        :return: The list of nightly rates
        """
        nightly_rates = []
        for i in range(self.nights):
            nightly_rates.append(get_night_rate(self.checkin + timezone.timedelta(days=i)))
        return nightly_rates

    @property
    def price(self):
        """
        :return: Total price for the stay
        """
        return sum(self.rates)

    def save(self, *args, **kwargs):
        self.rates = self.get_rates()
        try:
            value = self.value
            value.amount = self.price
            value.save()
        except ConceptValue.DoesNotExist:
            self.value = ConceptValue.objects.create(
                amount=self.price,
            )
        super().save(*args, **kwargs)

    @property
    def type(self):
        return gettext('Apartment Rental')

    @property
    def url(self):
       return '/apt-rentals/{}'.format(self.id)







