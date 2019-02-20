from __future__ import unicode_literals
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy
from django.utils import timezone
import uuid
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.postgres.fields import JSONField

User = get_user_model()

def get_default_currency():
    """
    Get the default currency
    :return:
    """
    try:
        return Currency.objects.get(default=True)
    except Currency.DoesNotExist:
        return None

def get_new_cashclose_code():
    """
    Generate a cashclose id code
    :return:
    """
    params = {
        'time': timezone.datetime.now().strftime('%m%d'),
        'uuid': uuid.uuid4().hex[:6],
    }
    code = 'CC%(time)s%(uuid)s' % params
    code = code.upper()
    # Check if already used
    try:
        CashClose.objects.get(code=code)
        return get_new_cashclose_code()
    except CashClose.DoesNotExist:
        return code

def get_new_transaction_code():
    """
    Generate a transaction id code
    :return:
    """
    params = {
        'time': timezone.datetime.now().strftime('%m%d'),
        'uuid': uuid.uuid4().hex[:6],
    }
    code = 'T%(time)s%(uuid)s' % params
    code = code.upper()
    # Check if already used
    try:
        Transaction.objects.get(code=code)
        return get_new_transaction_code()
    except Transaction.DoesNotExist:
        return code

def get_value_totals(values):
    """
    :return: The totals per currency for the given values
    """

    class DummyValue:
        def __init__(self, amount, credit, currency):
            self.amount = amount
            self.credit = credit
            self.currency = currency

    # A dictionary of currency:value totals to return
    totals = {}

    # For each concept
    for value in values:

        # Update existing currency total
        if value.currency in totals:
            # Add if credit
            if value.credit:
                totals[value.currency].amount += value.amount
            # Subtract if debit
            else:
                totals[value.currency].amount -= value.amount

        # Start new currency total
        else:
            totals[value.currency] = DummyValue(
                amount=value.amount if value.credit else value.amount*(-1),
                credit=True,
                currency=value.currency,
            )

    # Update totals credit value
    for _, value in totals.items():
        if value.amount < 0:
            value.credit = False
            value.amount *= -1

    # Return as ordered list of dummy values
    return [totals[k] for k in sorted(totals, key=totals.get)]


@python_2_unicode_compatible
class CashClose(models.Model):
    """
    A cash close records an end of day cash desk close operation.
    """
    code = models.CharField(verbose_name=gettext_lazy('Code'), max_length=32, unique=True, default=get_new_cashclose_code, editable=False)
    created = models.DateTimeField(verbose_name=gettext_lazy('Created'), auto_now_add=True)
    employee = models.ForeignKey(User, verbose_name=gettext_lazy('Employee'), editable=False)
    notes = models.TextField(max_length=1024, verbose_name=gettext_lazy('Notes'), blank=True, null=True)
    updated = models.DateTimeField(verbose_name=gettext_lazy('Updated'), auto_now=True)

    class Meta:
        verbose_name = gettext_lazy('Cash Desk Closure')
        verbose_name_plural = gettext_lazy('Cash Desk Closures')

    def __str__(self):
        return self.code


class Currency(models.Model):
    """
    Available currencies
    """
    name = models.CharField(max_length=256, verbose_name=gettext_lazy('Name'), blank=True, null=True)
    code_a = models.CharField(max_length=3, verbose_name=gettext_lazy('Alphabetic Code'), blank=True, null=True)
    code_n = models.CharField(max_length=3, verbose_name=gettext_lazy('Numeric Code'), blank=True, null=True)
    enabled = models.BooleanField(default=True, verbose_name=gettext_lazy('Enabled'))
    default = models.BooleanField(default=False, verbose_name=gettext_lazy('Default'))
    exchange_rate = models.FloatField(verbose_name=gettext_lazy('Exchange Rate'), blank=True, null=True)
    symbol = models.CharField(max_length=3, verbose_name=gettext_lazy('Symbol'), blank=True, null=True)

    class Meta:
        verbose_name = gettext_lazy('Currency')
        verbose_name_plural = gettext_lazy('Currencies')

    def __str__(self):
        items = [self.name, self.code_a, self.symbol, gettext_lazy('Currency')]
        return next(item for item in items if item is not None)


class ConceptValue(models.Model):
    """
    The amount of a given currency that a concept credits or debits
    """
    credit = models.BooleanField(verbose_name=gettext_lazy('Credit'), default=True)
    currency = models.ForeignKey(Currency, verbose_name=gettext_lazy('Currency'), default=get_default_currency, on_delete=models.PROTECT, related_name='values')
    amount = models.FloatField(verbose_name=gettext_lazy('Amount'))

    class Meta:
        verbose_name = gettext_lazy('Concept Value')
        verbose_name_plural = gettext_lazy('Concept Values')

    def __str__(self):
        return '{0} {1} {2}'.format(self.concept.code, self.currency.symbol, self.amount)


@python_2_unicode_compatible
class Transaction(models.Model):
    """
    A transaction records a single interaction between the host and
    a client. The interaction might involve multiple exchanges such as
    as renting, buying, reimbursing, deposit charge/return, etc.
    """
    apt_number = models.SmallIntegerField(blank=True, verbose_name=gettext_lazy('Apt Number'), null=True)
    cashclose = models.ForeignKey(CashClose, verbose_name=gettext_lazy('Cash Desk Close'), on_delete=models.SET_NULL, blank=True, null=True, related_name='transactions')
    code = models.CharField(verbose_name=gettext_lazy('Code'), max_length=32, unique=True, default=get_new_transaction_code, editable=False)
    client_address = models.TextField(max_length=512, verbose_name=gettext_lazy('Address'), blank=True, null=True)
    client_email = models.EmailField(verbose_name=gettext_lazy('Email'), blank=True, null=True)
    client_first_name = models.CharField(max_length=255, verbose_name=gettext_lazy('First Name'), blank=True, null=True)
    client_id = models.CharField(max_length=36, verbose_name=gettext_lazy('Passport/ID'), blank=True, null=True)
    client_last_name = models.CharField(max_length=255, verbose_name=gettext_lazy('Last Name'), blank=True, null=True)
    client_phone_number = models.CharField(max_length=14, verbose_name=gettext_lazy('Phone'), blank=True, null=True)
    closed = models.BooleanField(verbose_name=gettext_lazy('Closed'), default=False)
    closed_date = models.DateTimeField(verbose_name=gettext_lazy('Close Date'), blank=True, null=True)
    created = models.DateTimeField(verbose_name=gettext_lazy('Created'), auto_now_add=True)
    employee = models.ForeignKey(User, verbose_name=gettext_lazy('Employee'), editable=False)
    updated = models.DateTimeField(verbose_name=gettext_lazy('Updated'), auto_now=True)

    class Meta:
        verbose_name = gettext_lazy('Transaction')
        verbose_name_plural = gettext_lazy('Transactions')

    def __str__(self):
        return self.code

    @property
    def client(self):
        """
        :return: The client's full name if set
        """
        name = ''
        if self.client_first_name:
            name += self.client_first_name
            if self.client_last_name:
                name += ' '
        if self.client_last_name:
            name += self.client_last_name
        return name

    @property
    def description_short(self):
        """
        :return: A short single line description of the concept.
        """
        description = self.code
        if self.apt_number:
            description += ' '
            description += gettext_lazy('Apt') + ': {}'.format(self.apt_number)
        if self.client:
            description += ' '
            description += gettext_lazy('Client') + ': {}'.format(self.client)
        description += ' '
        description += gettext_lazy('Total') + ':'
        for value in self.totals:
            if not value.credit:
                description += 'db '
            description += ' {0} {1}'.format(value.currency.symbol, value.amount)
        return description

    @property
    def totals(self):
        """
        :return: The total amount of all concepts
        """
        return get_value_totals([concept.data.value for concept in self.concepts.all()])


@python_2_unicode_compatible
class Concept(models.Model):
    """
    A transaction concept records the type of exchange:
    Sale, rent, refund, etc...
    This model is liked one-to-one to concrete concepts that inherit BaseConcept
    """
    code = models.CharField(verbose_name=gettext_lazy('Code'), max_length=32, unique=True, editable=False)
    transaction = models.ForeignKey(Transaction, verbose_name=gettext_lazy('Transaction'), on_delete=models.CASCADE, related_name='concepts')

    class Meta:
        verbose_name = gettext_lazy('Abstract Concept')
        verbose_name_plural = gettext_lazy('Abstract Concepts')

    def __str__(self):
        return self.code


@python_2_unicode_compatible
class ConceptData(models.Model):
    """
    A transaction concept records the type of exchange:
    Sale, rent, refund, etc...
    This model is to be inherited by the required concept types
    """
    code = models.CharField(verbose_name=gettext_lazy('Code'), max_length=32, unique=True, editable=False)
    concept = models.OneToOneField(Concept, verbose_name=gettext_lazy('Abstract Concept'), on_delete=models.CASCADE, related_name='data')
    transaction = models.ForeignKey(Transaction, verbose_name=gettext_lazy('Transaction'), on_delete=models.CASCADE, related_name='baseconcepts')
    value = models.OneToOneField(ConceptValue, verbose_name=gettext_lazy('Value'), on_delete=models.CASCADE, related_name='concept')
    editing_concept = models.ForeignKey('self', verbose_name=gettext_lazy('Editing Concept'), related_name='editingconcept', on_delete=models.SET_NULL, blank=True, null=True)
    edited_concept = models.ForeignKey('self', verbose_name=gettext_lazy('Edited Concept'), related_name='editedconcept', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        abstract = True

    def code_initials(self):
        """
        :return: An acronym for code construction
        """
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        #super().delete(*args, **kwargs)
        self.concept.delete()

    def description_short(self):
        """
        :return: A short single line description of the concept.
        """
        raise NotImplementedError

    def description_long(self):
        """
        :return: A detailed (multiline if required) description of the concept.
        """
        raise NotImplementedError

    def save(self, *args, **kwargs):
        # Create the code if empty
        if not self.code:
            self.code = '{0}-{1}{2}'.format(self.transaction.code, self.code_initials, self.transaction.concepts.count() + 1)
        # Create the link concept if it does not exist
        try:
           assert self.concept
           self.concept.save()
        except Concept.DoesNotExist:
            self.concept = Concept.objects.create(
                code='{0}-C{1}'.format(self.transaction.code, self.transaction.concepts.count() + 1),
                transaction=self.transaction,
            )
        super().save(*args, **kwargs)

    def settings(self):
        """
        :return: The concept type settings
        """
        raise NotImplementedError

    @property
    def tax_amount(self):
        """
        The tax portion of the total
        """
        return self.value.amount - self.taxable_amount

    @property
    def taxable_amount(self):
        """
        The taxable amount according to vat percent rate in settings
        """
        return (self.value.amount * self.settings.vat_percent) / (self.settings.vat_percent + 1)

    def type(self):
        """
        :return: The type of concept, e.g.: Apartment Rental
        """
        raise NotImplementedError

    def url(self):
        """
        :return: The concept's base url
        """
        raise NotImplementedError


class SingletonModel(models.Model):
    """Singleton Django Model"""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Save object to the database. Removes all other entries if there
        are any.
        """
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        """
        Load object from the database. Failing that, create a new empty
        (default) instance of the object and return it (without saving it
        to the database).
        """

        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


@python_2_unicode_compatible
class ConceptSettings(SingletonModel):
    """
    Settings applicable to all transaction concept types
    """
    # VAT percent
    vat_percent = models.FloatField(verbose_name=gettext_lazy('VAT Percent'), default=0)
    # Required transaction fields when this type of concept is included
    apt_number = models.BooleanField(default=False, verbose_name=gettext_lazy('Apt Number Required'))
    client_address = models.BooleanField(default=False, verbose_name=gettext_lazy('Address Required'))
    client_email = models.BooleanField(default=False, verbose_name=gettext_lazy('Email Required'))
    client_first_name = models.BooleanField(default=False, verbose_name=gettext_lazy('First Name Required'))
    client_id = models.BooleanField(default=False, verbose_name=gettext_lazy('Passport/ID Required'))
    client_last_name = models.BooleanField(default=False, verbose_name=gettext_lazy('Last Name Required'))
    client_phone_number = models.BooleanField(default=False, verbose_name=gettext_lazy('Phone Required'))

    class Meta:
        abstract = True


