from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class DepositReturnsConfig(AppConfig):
    name = 'clickgestion.deposit_returns'
    verbose_name = gettext_lazy('Deposit Returns')

