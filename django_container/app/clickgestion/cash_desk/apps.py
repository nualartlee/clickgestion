from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class CashDeskConfig(AppConfig):
    name = 'clickgestion.cash_desk'
    verbose_name = gettext_lazy('Cash Desk')

