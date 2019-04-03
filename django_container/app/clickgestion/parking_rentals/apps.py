from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class ParkingRentalsConfig(AppConfig):
    name = 'clickgestion.parking_rentals'
    verbose_name = gettext_lazy('Parking Rentals')

