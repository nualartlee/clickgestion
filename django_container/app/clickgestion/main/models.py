from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Transaction(models.Model):
    operation = models.CharField(max_length=256, blank=True, null=True)
    timestamp = models.DateTimeField()
    user = models.ForeignKey(User, editable=False)
    http_request_data = models.CharField(max_length=256, blank=True, null=True)

    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return 'Transaction {0}'.format(self.id)

