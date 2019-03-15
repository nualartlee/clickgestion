from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class DepositsConfig(AppConfig):
    name = 'clickgestion.deposits'
    verbose_name = gettext_lazy('Deposits')

