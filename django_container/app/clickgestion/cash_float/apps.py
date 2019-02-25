from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class CashFloatConfig(AppConfig):
    name = 'clickgestion.cash_float'
    verbose_name = gettext_lazy('Cash Float')

