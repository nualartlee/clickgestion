from __future__ import unicode_literals
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy
from django.utils import timezone
import uuid
from django.utils.encoding import python_2_unicode_compatible

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


def get_breakdown_by_concept_type(transaction_set):
    """

    :param transaction_set: A set of transactions
    :return: A list of objects with the breakdown
    """
    class BreakdownType:
        def __init__(self, values, concept_count, totals, type):
            self.values = values
            self.concept_count = concept_count
            self.totals = totals
            self.type = type

    # Get breakdown by concept type
    breakdown = {}
    all_concepts = BaseConcept.objects.filter(transaction__in=transaction_set)
    for concept in all_concepts:

        # Update existing concept type total
        if concept.concept_type in breakdown:
            # Add value
            breakdown[concept.concept_type].values.append(concept.value)
            breakdown[concept.concept_type].concept_count += 1

        # Start new concept type total
        else:
            breakdown[concept.concept_type] = BreakdownType([concept.value], 1, None, concept.child._meta.verbose_name_plural)

    for concept_type in breakdown:
        breakdown[concept_type].totals = get_value_totals(breakdown[concept_type].values)

    return [ value for _, value in breakdown.items() ]


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
    #return [totals[k] for k in sorted(totals, key=totals.get)]
    return [v for v in totals.values()]


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
    notes = models.TextField(max_length=512, verbose_name=gettext_lazy('Notes'), blank=True, null=True)
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
        return get_value_totals([concept.value for concept in self.concepts.all()])


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
        return '{0} {1}'.format(self.currency.symbol, self.amount)


@python_2_unicode_compatible
class BaseConcept(models.Model):
    """
    A transaction concept records the type of exchange:
    Sale, rent, refund, etc...
    This model is to be inherited by the required concept types
    """
    # Human identification code
    code = models.CharField(verbose_name=gettext_lazy('Code'), max_length=32, unique=True, editable=False)
    # Required to access instances of child classes
    concept_class = models.CharField(verbose_name=gettext_lazy('Concept Class'), max_length=32, editable=False)
    # The concept that this one is editing
    edited_concept = models.ForeignKey('self', verbose_name=gettext_lazy('Edited Concept'), related_name='editingconcept', on_delete=models.CASCADE, blank=True, null=True)
    # The concept that is editing this one
    editing_concept = models.ForeignKey('self', verbose_name=gettext_lazy('Editing Concept'), related_name='editedconcept', on_delete=models.SET_NULL, blank=True, null=True)
    # The transaction this concept belongs to
    transaction = models.ForeignKey(Transaction, verbose_name=gettext_lazy('Transaction'), on_delete=models.CASCADE, related_name='concepts')
    # The value of this concept
    value = models.OneToOneField(ConceptValue, verbose_name=gettext_lazy('Value'), on_delete=models.CASCADE, related_name='concept')

    @property
    def child(self):
        """
        Get the instance of the child class inheriting from BaseConcept
        :return:
        """
        if not self.is_child:
            if self.concept_class:
                return getattr(self, self.concept_class)
        return self

    @property
    def code_initials(self):
        """
        :return: An acronym for code construction
        """
        if self.is_child:
            return self._code_initials
        return self.child._code_initials

    @property
    def class_type(self):
        """
        :return: The child class type
        """
        if self.is_child:
            return self.class_type
        return self.child.class_type

    @property
    def concept_type(self):
        """
        :return: The type of concept, e.g.: Apartment Rental
        """
        if self.is_child:
            return self._meta.verbose_name
        return self.child._meta.verbose_name

    @property
    def description_short(self):
        """
        :return: A short single line description of the concept.
        """
        if self.is_child:
            return self.description_short
        return self.child.description_short

    @property
    def is_child(self):
        return self.__class__ != BaseConcept

    @property
    def price(self):
        """
        :return: the price
        """
        if self.is_child:
            return self.price
        return self.child.price

    def save(self, *args, **kwargs):

        # Save the concept class
        self.concept_class = self._concept_class

        # Create the code if empty
        if not self.code:
            self.code = '{0}-{1}{2}'.format(self.transaction.code, self.code_initials, self.transaction.concepts.count() + 1)

        # Create the value if empty
        try:
            value = self.value
            value.save()
        except ConceptValue.DoesNotExist:
            value = ConceptValue.objects.create(
                amount=abs(self.price),
                credit=self.price >= 0
            )
            self.value = value

        # save
        super().save(*args, **kwargs)

    @property
    def settings(self):
        if self.is_child:
            return self._settings_class.objects.get_or_create()[0]
        return self.child._settings_class.objects.get_or_create()[0]

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

    @property
    def url(self):
        """
        :return: The concept's base url
        """
        if self.is_child:
            return self._url.format(self.child.code)
        return self.child._url.format(self.child.code)


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
    apt_number_required = models.BooleanField(default=False, verbose_name=gettext_lazy('Apt Number Required'))
    client_address_required = models.BooleanField(default=False, verbose_name=gettext_lazy('Address Required'))
    client_email_required = models.BooleanField(default=False, verbose_name=gettext_lazy('Email Required'))
    client_first_name_required = models.BooleanField(default=False, verbose_name=gettext_lazy('First Name Required'))
    client_id_required = models.BooleanField(default=False, verbose_name=gettext_lazy('Passport/ID Required'))
    client_last_name_required = models.BooleanField(default=False, verbose_name=gettext_lazy('Last Name Required'))
    client_phone_number_required = models.BooleanField(default=False, verbose_name=gettext_lazy('Phone Required'))
    notes_required = models.BooleanField(default=False, verbose_name=gettext_lazy('Notes Required'))
    apt_number_visible = models.BooleanField(default=True, verbose_name=gettext_lazy('Apt Number Visible'))
    client_address_visible = models.BooleanField(default=True, verbose_name=gettext_lazy('Address Visible'))
    client_email_visible = models.BooleanField(default=True, verbose_name=gettext_lazy('Email Visible'))
    client_first_name_visible = models.BooleanField(default=True, verbose_name=gettext_lazy('First Name Visible'))
    client_id_visible = models.BooleanField(default=True, verbose_name=gettext_lazy('Passport/ID Visible'))
    client_last_name_visible = models.BooleanField(default=True, verbose_name=gettext_lazy('Last Name Visible'))
    client_phone_number_visible = models.BooleanField(default=True, verbose_name=gettext_lazy('Phone Visible'))
    notes_visible = models.BooleanField(default=True, verbose_name=gettext_lazy('Notes Visible'))

    class Meta:
        abstract = True


