from __future__ import unicode_literals
from clickgestion.transactions.models import BaseConcept, ConceptValue, ConceptSettings
from django.utils.translation import gettext_lazy


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
    _url = '/cash-float/deposits/{}'
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
    _url = '/cash-float/withdrawals/{}'
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
