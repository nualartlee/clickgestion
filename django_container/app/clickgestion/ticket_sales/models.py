from __future__ import unicode_literals
from django.apps import apps
from clickgestion.concepts.models import BaseConcept, ConceptSettings, Currency, get_default_currency
from decimal import Decimal
from django.utils.translation import gettext, gettext_lazy
from django.db import models


class ShowCompany(models.Model):
    # Creation timestamp
    created = models.DateTimeField(verbose_name=gettext_lazy('Created'), auto_now_add=True)
    # Enabled
    enabled = models.BooleanField(verbose_name=gettext_lazy('Enabled'), default=True)
    # Name
    name = models.CharField(verbose_name=gettext_lazy('Name'), max_length=64, unique=True)
    # Last update timestamp
    updated = models.DateTimeField(verbose_name=gettext_lazy('Updated'), auto_now=True)

    class Meta:
        verbose_name = gettext_lazy('Tour/Show Company')
        verbose_name_plural = gettext_lazy('Tour/Show Companies')

    def __str__(self):
        return self.name


class Show(models.Model):
    # Company
    company = models.ForeignKey(
        'ticket_sales.ShowCompany',
        verbose_name=gettext_lazy('Company'),
        on_delete=models.CASCADE,
        related_name='shows',
    )
    # Creation timestamp
    created = models.DateTimeField(verbose_name=gettext_lazy('Created'), auto_now_add=True)
    # Currency
    currency = models.ForeignKey(
        'concepts.Currency', verbose_name=gettext_lazy('Currency'), default=get_default_currency,
        on_delete=models.PROTECT, related_name='shows')
    # A specific date is required
    date_required = models.BooleanField(verbose_name=gettext_lazy('Date Required'), default=False)
    # Enabled
    enabled = models.BooleanField(verbose_name=gettext_lazy('Enabled'), default=True)
    # Name
    name = models.CharField(verbose_name=gettext_lazy('Name'), max_length=64, unique=True)
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
    price_per_adult = models.DecimalField(verbose_name=gettext_lazy('Price Per Adult'),
                                          default=10, decimal_places=2, max_digits=12)
    # Price per child
    price_per_child = models.DecimalField(verbose_name=gettext_lazy('Price Per Child'),
                                          default=10, decimal_places=2, max_digits=12)
    # Price per senior
    price_per_senior = models.DecimalField(verbose_name=gettext_lazy('Price Per Senior'),
                                           default=10, decimal_places=2, max_digits=12)
    # Price per unit
    price_per_unit = models.DecimalField(verbose_name=gettext_lazy('Price Per Unit'),
                                         default=10, decimal_places=2, max_digits=12)
    # Price can be set on transaction
    variable_price = models.BooleanField(verbose_name=gettext_lazy('Variable Price'), default=False)
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
    adults = models.SmallIntegerField(verbose_name=gettext_lazy('Adults'), default=2)
    # Number of children
    children = models.SmallIntegerField(verbose_name=gettext_lazy('Children'), default=0)
    # A specific date is required
    date_required = models.BooleanField(verbose_name=gettext_lazy('Date Required'), default=False)
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
    price_per_adult = models.DecimalField(verbose_name=gettext_lazy('Price Per Adult'),
                                          default=0, decimal_places=2, max_digits=12)
    # Price per child
    price_per_child = models.DecimalField(verbose_name=gettext_lazy('Price Per Child'),
                                          default=0, decimal_places=2, max_digits=12)
    # Price per senior
    price_per_senior = models.DecimalField(verbose_name=gettext_lazy('Price Per Senior'),
                                           default=0, decimal_places=2, max_digits=12)
    # Price per unit
    price_per_unit = models.DecimalField(verbose_name=gettext_lazy('Price Per Unit'),
                                         default=0, decimal_places=2, max_digits=12)
    # Number of seniors
    seniors = models.SmallIntegerField(verbose_name=gettext_lazy('Seniors'), default=0)
    # The show
    show = models.ForeignKey(
        'ticket_sales.Show',
        verbose_name=gettext_lazy('Tour/Show'),
        on_delete=models.CASCADE,
        related_name='tickets',
    )
    # Number of units
    units = models.SmallIntegerField(verbose_name=gettext_lazy('Units'), default=1)

    # BaseConcept settings
    _url = '/ticket-sales/{}'
    _code_initials = 'TS'
    _concept_class = 'ticketsale'
    _settings_class = TicketSaleSettings
    _verbose_name = 'Ticket Sale'

    class Meta:
        verbose_name = gettext_lazy('Ticket Sale')
        verbose_name_plural = gettext_lazy('Ticket Sales')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.code

    @property
    def name(self):
        return self._meta.verbose_name

    @property
    def description_short(self):
        desc = '{} {}: {}'.format(self.name, self.show.company.name, self.show.name)
        # Date required
        if self.date_required or self.per_night:
            desc += ' {}'.format(self.start_date.strftime('%a, %d %b %Y'))
        # Per night
        if self.per_night:
            desc += ' - {}'.format(self.end_date.strftime('%a, %d %b %Y'))
        # Per transaction
        if not (self.per_adult or self.per_child or self.per_senior or self.per_unit):
            pass
        # Per unit
        if self.per_unit:
            if self.units == 1:
                text = gettext_lazy('%(units)s Unit x %(price)s;')
            else:
                text = gettext_lazy('%(units)s Units x %(price)s;')
            desc += ' {}'.format(text % {'units': self.units, 'price': self.price_per_unit})
        # Per adult
        if self.per_adult:
            if self.adults == 1:
                text = gettext_lazy('%(adults)s Adult x %(price)s;')
            else:
                text = gettext_lazy('%(adults)s Adults x %(price)s;')
            desc += ' {}'.format(text % {'adults': self.adults, 'price': self.price_per_adult})
        # Per child
        if self.per_child:
            if self.children == 1:
                text = gettext_lazy('%(children)s Child x %(price)s;')
            else:
                text = gettext_lazy('%(children)s Children x %(price)s;')
            desc += ' {}'.format(text % {'children': self.children, 'price': self.price_per_child})
        # Per senior
        if self.per_senior:
            if self.seniors == 1:
                text = gettext_lazy('%(seniors)s Senior x %(price)s;')
            else:
                text = gettext_lazy('%(seniors)s Seniors x %(price)s;')
            desc += ' {}'.format(text % {'seniors': self.seniors, 'price': self.price_per_senior})
        return desc

    def get_value(self):
        """
        :return:ConceptValue: Total price for the tickets
        """
        # Return the saved value if the transaction is closed
        if self.transaction.closed:
            return self.value

        # Per night
        amount = Decimal(0)
        if self.per_night:
            nights = Decimal((self.end_date - self.start_date).days)
        else:
            nights = Decimal(1)
        # Per transaction
        if not (self.per_adult or self.per_child or self.per_senior or self.per_unit):
            amount += self.price_per_unit * nights
        # Per unit
        if self.per_unit:
            amount += self.price_per_unit * self.units * nights
        # Per adult
        if self.per_adult:
            amount += self.price_per_adult * self.adults * nights
        # Per child
        if self.per_child:
            amount += self.price_per_child * self.children * nights
        # Per senior
        if self.per_senior:
            amount += self.price_per_senior * self.seniors * nights

        value_model = apps.get_model('concepts.ConceptValue')
        try:
            self.value.amount = amount
        except value_model.DoesNotExist:
            self.value = value_model(amount=amount)
        return self.value

    #def save(self):

    #    self.date_required = self.show.date_required
    #    self.per_adult = self.show.per_adult
    #    self.per_child = self.show.per_child
    #    self.per_night = self.show.per_night
    #    self.per_senior = self.show.per_senior
    #    self.per_unit = self.show.per_unit

    #    #if not self.price_per_adult:
    #    #    self.price_per_adult = self.show.price_per_adult
    #    #if not self.price_per_child:
    #    #    self.price_per_child = self.show.price_per_child
    #    #if not self.price_per_senior:
    #    #    self.price_per_senior = self.show.price_per_senior
    #    #if not self.price_per_unit:
    #    #    self.price_per_unit = self.show.price_per_unit

    #    if not self.per_night:
    #        self.end_date = self.start_date
    #    super().save()
