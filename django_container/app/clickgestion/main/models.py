from __future__ import unicode_literals
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Transaction(models.Model):
    """
    A transaction records a single interaction between the host and
    a client. The interaction might involve multiple exchanges such as
    as renting, buying, reimbursing, deposit charge/return, etc.
    """
    employee = models.ForeignKey(User, editable=False)
    client_name = models.CharField(max_length=255)
    apt_number = models.SmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'Transaction {0}'.format(self.id)


class Concept(models.Model):
    """
    A transaction concept records the type of exchange:
    Sale, rent, refund, etc...
    This model is to be inherited by the required concept types
    """
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)

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
