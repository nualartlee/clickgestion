from __future__ import unicode_literals
from django.apps import apps
from clickgestion.concepts.models import BaseConcept, ConceptSettings
from django.utils.translation import gettext, gettext_lazy
from django.db import models


class Show(models.Model):
    # Creation timestamp
    created = models.DateTimeField(verbose_name=gettext_lazy('Created'), auto_now_add=True)
    # A specific date is required
    date_required = models.BooleanField(verbose_name=gettext_lazy('Date Required'), default=False)
    # Name
    name = models.CharField(verbose_name=gettext_lazy('Name'), max_length=64)
    # Tickets are booked per adult
    per_adult = models.BooleanField(verbose_name=gettext_lazy('Book Per Adult'), default=False)
    # Tickets are booked per child
    per_child = models.BooleanField(verbose_name=gettext_lazy('Book Per Child'), default=False)
    # Tickets are booked per night
    per_night = models.BooleanField(verbose_name=gettext_lazy('Book Per Night'), default=False)
    # Tickets are booked per senior
    per_senior = models.BooleanField(verbose_name=gettext_lazy('Book Per Senior'), default=False)
    # Tickets are booked per unit
    per_unit = models.BooleanField(verbose_name=gettext_lazy('Book Per Unit'), default=False)
    # Price per adult
    price_per_adult = models.FloatField(verbose_name=gettext_lazy('Price Per Adult'), blank=True, null=True)
    # Price per child
    price_per_child = models.FloatField(verbose_name=gettext_lazy('Price Per Child'), blank=True, null=True)
    # Price per senior
    price_per_senior = models.FloatField(verbose_name=gettext_lazy('Price Per Senior'), blank=True, null=True)
    # Last update timestamp
    updated = models.DateTimeField(verbose_name=gettext_lazy('Updated'), auto_now=True)

    class Meta:
        verbose_name = gettext_lazy('Tour/Show')
        verbose_name_plural = gettext_lazy('Tours/Shows')

    def __str__(self):
        return self.name

    @property
    def per_transaction(self):
        """
        Sells one unit only per transaction
        :return: True if the show is one unit per transaction only
        """
        return not(self.per_adult or self.per_child or self.per_senior or self.per_unit)


class TicketSaleSettings(ConceptSettings):
    """
    Ticket Sale Concept Settings
    """
    class Meta:
        verbose_name = gettext_lazy('Ticket Sale Settings')
        verbose_name_plural = gettext_lazy('Ticket Sale Settings')


class TicketSale(BaseConcept):
    """
    Transaction Concept
    Ticket sale
    """
    # Number of adults
    adults = models.SmallIntegerField(verbose_name=gettext_lazy('Adults'), default=1)
    # Number of children
    children = models.SmallIntegerField(verbose_name=gettext_lazy('Children'), default=0)
    # Number of seniors
    seniors = models.SmallIntegerField(verbose_name=gettext_lazy('Seniors'), default=0)
    # The show
    show = models.ForeignKey(
        'ticket_sales.Show',
        verbose_name=gettext_lazy('Tour/Show'),
        on_delete=models.CASCADE,
        related_name='tickets',
    )

    # BaseConcept settings
    _url = '/ticket-sales/{}'
    _code_initials = 'TS'
    _concept_class = 'ticketsale'
    _settings_class = TicketSaleSettings
    _verbose_name = 'Ticket Sale'

    class Meta:
        verbose_name = gettext_lazy('Ticket Sale')
        verbose_name_plural = gettext_lazy('Ticket Sales')

    def __str__(self):
        return self.code

    @property
    def name(self):
        return self._meta.verbose_name

    @property
    def description_short(self):
        desc = '{} {} '.format(self.name, self.show.name)
        # Date required
        if self.show.date_required or self.show.per_night:
            desc += ':{}'.format(self.start_date.strftime('%a, %d %b %Y'))
        # Per night
        if self.show.per_night:
            desc += ' - {}'.format(self.start_date.strftime('%a, %d %b %Y'))
        # Per transaction
        if self.show.per_transaction:
            pass
        # Per unit (use adults)
        if self.show.per_unit:
            desc += ' {}'.format(gettext_lazy('Units: %(units)s') % {'units': self.adults})
        # Per adult
        if self.show.per_adult:
            desc += ' {}'.format(gettext_lazy('Adults: %(units)s') % {'units': self.adults})
        # Per child
        if self.show.per_child:
            desc += ' {}'.format(gettext_lazy('Children: %(units)s') % {'units': self.children})
        # Per senior
        if self.show.per_senior:
            desc += ' {}'.format(gettext_lazy('Seniors: %(units)s') % {'units': self.seniors})
        return desc

    def get_value(self):
        """
        :return:ConceptValue: Total price for the tickets
        """
        # Return the saved value if the transaction is closed
        if self.transaction.closed:
            return self.value

        # Per night
        amount = 0
        if self.show.per_night:
            nights = (self.end_date - self.start_date).days
        else:
            nights = 1
        # Per transaction
        if self.show.per_transaction:
            amount += self.show.price_per_adult * nights
        # Per adult or unit (use adults)
        if self.show.per_adult or self.show.per_unit:
            amount += self.show.price_per_adult * self.adults * nights
        # Per child
        if self.show.per_child:
            amount += self.show.price_per_child * self.children * nights
        # Per senior
        if self.show.per_senior:
            amount += self.show.price_per_senior * self.seniors * nights

        value_model = apps.get_model('concepts.ConceptValue')
        try:
            self.value.amount = amount
        except value_model.DoesNotExist:
            self.value = value_model(amount=amount)
        return self.value
