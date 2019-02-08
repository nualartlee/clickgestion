from clickgestion.apartment_rentals.models import ApartmentRental, NightRateRange, get_night_rate
from clickgestion.main.test import CustomTestCase
from django.utils import timezone


class TestNightRateRange(CustomTestCase):

    def test_model(self):
        assert self.night_rate_range

    def test_get_night_rate_ok(self):
        assert get_night_rate(timezone.datetime.today)


class TestApartmentRental(CustomTestCase):

    def test_model(self):
        assert self.apartment_rental