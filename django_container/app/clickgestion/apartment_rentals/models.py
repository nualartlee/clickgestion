from __future__ import unicode_literals
from django.contrib.postgres.fields import ArrayField
from clickgestion.main.models import Concept, ConceptValue
from django.utils.translation import gettext
from django.db import models
from django.utils import timezone


class NightRateRange(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    monday = models.FloatField()
    tuesday = models.FloatField()
    wednesday = models.FloatField()
    thursday = models.FloatField()
    friday = models.FloatField()
    saturday = models.FloatField()
    sunday = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


def get_night_rate(date):
    """
    Get the rate  for a given date.
    :param date: Date
    :return: Cost for the night (always assumed to be default currency)
    """
    # Find the last (latest) rate range that the given date falls in
    rate = NightRateRange.objects.filter(start_date__lte=date, end_date__gte=date).latest('id')
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


class ApartmentRental(Concept):
    """
    Transaction Concept
    Apartment rental
    """
    # Arrival date
    checkin = models.DateField()
    # Departure date
    checkout = models.DateField()
    # Ordered list of daily rates
    rates = ArrayField(models.FloatField())

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
        :return: The list of daily rates
        """
        daily_rates = []
        for i in range(self.nights):
            daily_rates.append(get_night_rate(self.checkin + timezone.timedelta(days=i)))
        return daily_rates

    @property
    def price(self):
        """
        :return: Total price for the stay
        """
        return sum(self.rates)

    def save(self, *args, **kwargs):
        self.rates = self.get_rates()
        super().save(*args, **kwargs)

    @property
    def type(self):
        return gettext('Apartment Rental')








