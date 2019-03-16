from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from clickgestion.concepts.totalizers import get_value_totals
from django.utils.translation import gettext_lazy
from django.db import models
from django.contrib.auth.models import Permission
import re
from django.utils import timezone
import uuid

User = get_user_model()


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


class Transaction(models.Model):
    """
    A transaction records a single interaction between the host and
    a client. The interaction might involve multiple exchanges such as
    as renting, buying, reimbursing, deposit charge/return, etc.
    """
    apt_number = models.SmallIntegerField(blank=True, verbose_name=gettext_lazy('Apt Number'), null=True)
    cashclose = models.ForeignKey(
        'cash_desk.cashclose',
        verbose_name=gettext_lazy('Cash Desk Close'),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='transactions',
    )
    code = models.CharField(
        verbose_name=gettext_lazy('Code'),
        max_length=32, unique=True,
        default=get_new_transaction_code,
        editable=False,
    )
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
    def client_signature_required(self):
        for concept in self.concepts.all():
            if concept.settings.client_signature_required:
                return True
        return False

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
    def employee_signature_required(self):
        for concept in self.concepts.all():
            if concept.settings.employee_signature_required:
                return True
        return False

    def get_all_permissions(self):
        """
        :return: The permissions for this transaction according to included concepts
        """
        # Get all permissions
        perms = Permission.objects.all().values_list('content_type__app_label', 'codename').order_by()
        perms = set("%s.%s" % (ct, name) for ct, name in perms)

        # Filter by selected concepts
        if self.concepts.all().exists():
            for concept in self.concepts.all():
                # Get common permissions (set intersection)
                perms = perms & concept.get_all_permissions()

        # Return the set
        return perms

    @property
    def next_concept_id(self):
        next_id = 1
        if self.concepts.exists():
            for concept in self.concepts.values('code'):
                result = re.search('\d+$', concept['code'])
                code_id = int(result.group())
                if code_id >= next_id:
                    next_id = code_id + 1
        return next_id

    @property
    def title(self):
        accounting_groups = self.concepts.values_list('accounting_group', flat=True).distinct()
        if 'Production' in accounting_groups:
            return gettext_lazy('Invoice')
        if 'Deposits' in accounting_groups:
            return gettext_lazy('Deposit Transaction')
        if 'Cash' in accounting_groups:
            return gettext_lazy('Cash Management')
        return gettext_lazy('Transaction')


    @property
    def totals(self):
        """
        :return: The total amount of all concepts
        """
        return get_value_totals(self.concepts.all())
