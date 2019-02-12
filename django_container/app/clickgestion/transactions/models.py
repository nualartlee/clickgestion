from __future__ import unicode_literals
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext

User = get_user_model()


class Transaction(models.Model):
    """
    A transaction records a single interaction between the host and
    a client. The interaction might involve multiple exchanges such as
    as renting, buying, reimbursing, deposit charge/return, etc.
    """
    employee = models.ForeignKey(User, editable=False)
    client_first_name = models.CharField(max_length=255, blank=True, null=True)
    client_last_name = models.CharField(max_length=255, blank=True, null=True)
    apt_number = models.SmallIntegerField(blank=True, null=True)
    closed = models.BooleanField(default=False)
    closed_time = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'Transaction {0}'.format(self.id)

    @property
    def client(self):
        """
        :return: The client's full name if set
        """
        if self.client_first_name or self.client_last_name:
            name = '{0} {1}'.format(self.client_first_name, self.client_last_name)
        else:
            name = gettext('Not Set')
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



class Concept(models.Model):
    """
    A transaction concept records the type of exchange:
    Sale, rent, refund, etc...
    This model is liked one-to-one to concrete concepts that inherit BaseConcept
    """
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='concepts')


class ConceptData(models.Model):
    """
    A transaction concept records the type of exchange:
    Sale, rent, refund, etc...
    This model is to be inherited by the required concept types
    """
    concept = models.OneToOneField(Concept, on_delete=models.CASCADE, related_name='data')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='baseconcepts')

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
