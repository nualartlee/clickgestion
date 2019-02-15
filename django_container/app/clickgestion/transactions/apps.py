from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class TransactionsConfig(AppConfig):
    name = 'clickgestion.transactions'
    verbose_name = gettext_lazy('Transactions')

