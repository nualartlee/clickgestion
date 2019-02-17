from __future__ import unicode_literals
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext, gettext_lazy, ugettext, ugettext_lazy
from django.utils import timezone
import uuid
from django.utils.encoding import python_2_unicode_compatible

User = get_user_model()

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
    client_address = models.TextField(max_length=1024, verbose_name=gettext_lazy('Address'), blank=True, null=True)
    client_email = models.EmailField(verbose_name=gettext_lazy('Email'), blank=True, null=True)
    client_first_name = models.CharField(max_length=255, verbose_name=gettext_lazy('First Name'), blank=True, null=True)
    client_id = models.CharField(max_length=36, verbose_name=gettext_lazy('Passport/ID'), blank=True, null=True)
    client_last_name = models.CharField(max_length=255, verbose_name=gettext_lazy('Last Name'), blank=True, null=True)
    client_phone_number = models.CharField(max_length=14, verbose_name=gettext_lazy('Phone'), blank=True, null=True)
    closed = models.BooleanField(verbose_name=gettext_lazy('Closed'), default=False)
    closed_time = models.DateTimeField(verbose_name=gettext_lazy('Close Time'), blank=True, null=True)
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
        description = gettext('Transaction #:{0} Apt:{1} Client: {2} Concepts: {3} Total: {4}'.format(
            self.id, self.apt_number, self.client, self.concepts.all().count(), self.total,
        ))
        return description

    @property
    def total(self):
        """
        :return: The total amount of all concepts
        """
        total = 0
        for concept in self.concepts.all():
            total += concept.data.price
        return total


@python_2_unicode_compatible
class Concept(models.Model):
    """
    A transaction concept records the type of exchange:
    Sale, rent, refund, etc...
    This model is liked one-to-one to concrete concepts that inherit BaseConcept
    """
    transaction = models.ForeignKey(Transaction, verbose_name=gettext_lazy('Transaction'), on_delete=models.CASCADE, related_name='concepts')

    class Meta:
        verbose_name = gettext_lazy('Abstract Concept')
        verbose_name_plural = gettext_lazy('Abstract Concepts')

    def __str__(self):
        return '{0}-C{1}'.format(self.transaction.code, self.id)


@python_2_unicode_compatible
class ConceptData(models.Model):
    """
    A transaction concept records the type of exchange:
    Sale, rent, refund, etc...
    This model is to be inherited by the required concept types
    """
    concept = models.OneToOneField(Concept, verbose_name=gettext_lazy('Abstract Concept'), on_delete=models.CASCADE, related_name='data')
    transaction = models.ForeignKey(Transaction, verbose_name=gettext_lazy('Transaction'), on_delete=models.CASCADE, related_name='baseconcepts')

    class Meta:
        abstract = True

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

    def save(self, *args, **kwargs):
        try:
           assert self.concept
           self.concept.save()
        except Concept.DoesNotExist:
            self.concept = Concept.objects.create(
                transaction=self.transaction,
            )
        super().save(*args, **kwargs)


class Currency(models.Model):
    short_name = models.CharField(max_length=32, blank=True, null=True)
    long_name = models.CharField(max_length=256, blank=True, null=True)
    enabled = models.BooleanField(default=True)
    default = models.BooleanField(default=False)
    exchange_rate = models.FloatField()


class ConceptValue(models.Model):
    credit = models.BooleanField()
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    amount = models.FloatField()
