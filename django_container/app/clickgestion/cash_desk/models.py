from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy
from django.db import models
from django.utils import timezone
import uuid
from clickgestion.transactions.models import BaseConcept, ConceptSettings

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
    _url = '/cash-desk/deposits/{}'
    _settings_class = CashFloatDepositSettings
    _code_initials = 'CFD'
    _concept_class = 'cashfloatdeposit'

    class Meta:
        verbose_name = gettext_lazy('Cash Float Deposit')
        verbose_name_plural = gettext_lazy('Cash Float Deposits')

    def __str__(self):
        return self.code

    @property
    def description_short(self):
        desc = self._meta.verbose_name + ' ' + self.code
        return desc

    @property
    def price(self):
        """
        :return: Total price for the stay
        """
        return self.value.amount


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

    class Meta:
        verbose_name = gettext_lazy('Cash Float Withdrawal')
        verbose_name_plural = gettext_lazy('Cash Float Withdrawals')

    def __str__(self):
        return self.code

    @property
    def description_short(self):
        desc = self._meta.verbose_name + ' ' + self.code
        return desc

    @property
    def price(self):
        """
        :return: Total price for the stay
        """
        return self.value.amount


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

    return [value for _, value in breakdown.items()]


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
    return [v for v in totals.values()]


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

