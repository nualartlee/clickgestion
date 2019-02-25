from __future__ import unicode_literals
from clickgestion.transactions.models import BaseConcept, ConceptValue, ConceptSettings
from django.utils.translation import gettext_lazy
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class CashFloatDeposit(BaseConcept):
    """
    Cash Float Deposit
    Increase the cash float adding money
    """

    class Meta:
        verbose_name = gettext_lazy('Cash Float Deposit')
        verbose_name_plural = gettext_lazy('Cash Float Deposits')

    def __init__(self, *args, **kwargs):
        #BaseConcept settings
        self._url = '/cash-float/deposits/{}'
        self._settings_class = CashFloatDepositSettings
        self._code_initials = 'CFD'
        self._concept_class = 'cashfloatdeposit'
        super().__init__(*args, **kwargs)

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


class CashFloatDepositSettings(ConceptSettings):
    """
    Apartment Rental Concept Settings
    """
    class Meta:
        verbose_name = gettext_lazy('Cash Float Deposit Settings')
        verbose_name_plural = gettext_lazy('Cash Float Deposit Settings')


@python_2_unicode_compatible
class CashFloatWithdrawal(BaseConcept):
    """
    Cash Float Withdrawal
    Decrease the cash float by taking money
    """

    class Meta:
        verbose_name = gettext_lazy('Cash Float Withdrawal')
        verbose_name_plural = gettext_lazy('Cash Float Withdrawals')

    def __init__(self, *args, **kwargs):
        #BaseConcept settings
        self._url = '/cash-float/withdrawals/{}'
        self._settings_class = CashFloatWithdrawalSettings
        self._code_initials = 'CFW'
        self._concept_class = 'cashfloatwithdrawal'
        super().__init__(*args, **kwargs)

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
