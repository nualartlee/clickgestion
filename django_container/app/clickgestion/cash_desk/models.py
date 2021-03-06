from __future__ import unicode_literals
from django.apps import apps
from clickgestion.concepts.models import BaseConcept, ConceptSettings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy
from django.db import models
from django.utils import timezone
from clickgestion.concepts import totalizers
import uuid

User = get_user_model()


class CashFloatDepositSettings(ConceptSettings):
    """
    Apartment Rental Concept Settings
    """
    class Meta:
        verbose_name = gettext_lazy('Cash Float Deposit Settings')
        verbose_name_plural = gettext_lazy('Cash Float Deposit Settings')


class CashFloatDeposit(BaseConcept):
    """
    Cash Float Deposit
    Increase the cash float adding money
    """

    #BaseConcept settings
    _code_initials = 'CFD'
    _concept_class = 'cashfloatdeposit'
    _settings_class = CashFloatDepositSettings
    _url = '/cash-desk/deposits/{}'
    _verbose_name = 'Cash Float Deposit'

    class Meta:
        verbose_name = gettext_lazy('Cash Float Deposit')
        verbose_name_plural = gettext_lazy('Cash Float Deposits')

    def __str__(self):
        return self.code

    @property
    def description_short(self):
        desc = '{} {}{}'.format(
            self._meta.verbose_name,
            self.value.currency.symbol,
            self.value.amount,
        )
        return desc

    @property
    def name(self):
        return self._meta.verbose_name


class CashFloatWithdrawalSettings(ConceptSettings):
    """
    CashFloatWithdrawal Concept Settings
    """
    class Meta:
        verbose_name = gettext_lazy('Cash Float Withdrawal Settings')
        verbose_name_plural = gettext_lazy('Cash Float Withdrawal Settings')


class CashFloatWithdrawal(BaseConcept):
    """
    Cash Float Withdrawal
    Decrease the cash float by taking money
    """

    #BaseConcept settings
    _url = '/cash-desk/withdrawals/{}'
    _settings_class = CashFloatWithdrawalSettings
    _code_initials = 'CFW'
    _concept_class = 'cashfloatwithdrawal'
    _verbose_name = 'Cash Float Withdrawal'

    class Meta:
        verbose_name = gettext_lazy('Cash Float Withdrawal')
        verbose_name_plural = gettext_lazy('Cash Float Withdrawals')

    def __str__(self):
        return self.code

    @property
    def description_short(self):
        desc = '{} {}{}'.format(
            self._meta.verbose_name,
            self.value.currency.symbol,
            self.value.amount,
        )
        return desc

    @property
    def name(self):
        return self._meta.verbose_name


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
        return get_new_cashclose_code()  # pragma: no cover
    except CashClose.DoesNotExist:
        return code


class CashClose(models.Model):
    """
    A cash close records an end of day cash desk close operation.
    """
    # Cash desk is closed
    closed = models.BooleanField(verbose_name=gettext_lazy('Closed'), default=False)
    code = models.CharField(
        verbose_name=gettext_lazy('Code'), max_length=32, unique=True, default=get_new_cashclose_code, editable=False)
    created = models.DateTimeField(verbose_name=gettext_lazy('Created'), auto_now_add=True)
    employee = models.ForeignKey(User, verbose_name=gettext_lazy('Employee'), editable=False)
    notes = models.TextField(max_length=1024, verbose_name=gettext_lazy('Notes'), blank=True, null=True)
    updated = models.DateTimeField(verbose_name=gettext_lazy('Updated'), auto_now=True)

    class Meta:
        verbose_name = gettext_lazy('Cash Desk Closure')
        verbose_name_plural = gettext_lazy('Cash Desk Closures')

    def __str__(self):
        return self.code

    @property
    def balance(self):
        return totalizers.get_value_totals(self.concepts)

    @property
    def breakdown_by_accounting_group(self):
        return totalizers.get_breakdown_by_accounting_group(self.concepts)

    @property
    def breakdown_by_concept_type(self):
        return totalizers.get_breakdown_by_concept_type(self.concepts)

    @property
    def breakdowns_by_accounting_group_by_employee(self):
        return totalizers.get_breakdowns_by_accounting_group_by_employee(self.concepts)

    @property
    def breakdowns_by_concept_type_by_employee(self):
        return totalizers.get_breakdowns_by_concept_type_by_employee(self.concepts)

    @property
    def breakdowns(self):
        breakdowns = [
            self.deposits_in_holding_breakdown,
            self.breakdown_by_accounting_group,
            self.breakdown_by_concept_type,
        ]
        breakdowns += self.breakdowns_by_accounting_group_by_employee
        breakdowns += self.breakdowns_by_concept_type_by_employee
        return breakdowns

    @property
    def concepts(self):
        return BaseConcept.objects.filter(transaction__cashclose=self)

    @property
    def deposits_in_holding_breakdown(self):
        return totalizers.get_deposits_in_holding_breakdown(datetime=self.created)

    @property
    def deposits_in_holding_totals(self):
        return totalizers.get_deposits_in_holding_totals(datetime=self.created)

    def save(self, *args, **kwargs):

        # Return if already closed
        if self.closed:
            return

        # Save the cash desk close
        self.closed = True
        super().save(*args, **kwargs)

        # Save cashclose on all closed transactions
        closed_transactions = apps.get_model('transactions.Transaction').objects.filter(closed=True, cashclose=None)
        closed_transactions.update(cashclose=self)

        # Deposit the balance as the first transaction of the next cash desk
        transaction = apps.get_model('transactions.Transaction')(
            employee=self.employee,
            notes='Cash Close Deposit',
        )
        transaction.save()
        for dummy_value in self.balance:
            value = apps.get_model('concepts.ConceptValue')(
                amount=dummy_value.amount,
                currency=dummy_value.currency,
            )
            deposit = CashFloatDeposit(transaction=transaction, value=value)
            deposit.save()
        transaction.close(self.employee)


