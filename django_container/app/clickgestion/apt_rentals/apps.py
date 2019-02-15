from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class AptRentalsConfig(AppConfig):
    name = 'clickgestion.apt_rentals'
    verbose_name = gettext_lazy('Apartment Rentals')

