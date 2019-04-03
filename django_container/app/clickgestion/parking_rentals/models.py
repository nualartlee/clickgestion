from __future__ import unicode_literals
from django.apps import apps
from clickgestion.concepts.models import BaseConcept, ConceptSettings
from django.utils.translation import gettext, gettext_lazy
from django.db import models


class ParkingRentalSettings(ConceptSettings):
    """
    Parking Rental Concept Settings
    """
    # Amount per night
    amount_per_night = models.FloatField(verbose_name=gettext_lazy('Amount Per Night'), default=10)

    class Meta:
        verbose_name = gettext_lazy('Parking Rental Settings')
        verbose_name_plural = gettext_lazy('Parking Rental Settings')


class ParkingRental(BaseConcept):
    """
    Transaction Concept
    Parking rental
    """

    # BaseConcept settings
    _url = '/parking-rentals/{}'
    _code_initials = 'PR'
    _concept_class = 'parkingrental'
    _settings_class = ParkingRentalSettings
    _verbose_name = 'Parking Rental'

    class Meta:
        verbose_name = gettext_lazy('Parking Rental')
        verbose_name_plural = gettext_lazy('Parking Rentals')

    def __str__(self):
        return self.code

    @property
    def name(self):
        return self._meta.verbose_name

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
        }
        desc = gettext('Parking Rental: %(start_date)s - %(end_date)s')
        return desc % data

    def get_current_rates(self):
        """
        :return: The list of nightly rates
        """
        nightly_rates = []
        for i in range(self.nights):
            nightly_rates.append(self.settings.amount_per_night)
        return nightly_rates

    def get_value(self):
        """
        :return:ConceptValue: Total price for the stay
        """
        # Return the saved value if the transaction is closed
        if self.transaction.closed:
            return self.value
        # Get the current value
        rates = self.get_current_rates()
        value_model = apps.get_model('concepts.ConceptValue')
        try:
            self.value.amount = sum(rates)
        except value_model.DoesNotExist:
            self.value = value_model(amount=sum(rates))
        return self.value
