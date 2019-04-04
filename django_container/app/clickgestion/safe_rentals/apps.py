from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class SafeRentalsConfig(AppConfig):
    name = 'clickgestion.safe_rentals'
    verbose_name = gettext_lazy('Safe Rentals')

