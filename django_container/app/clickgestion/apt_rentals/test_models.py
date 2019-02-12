from clickgestion.apt_rentals.models import ApartmentRental, NightRateRange, get_night_rate
from clickgestion.core.test import CustomTestCase
from django.utils import timezone


class TestNightRateRange(CustomTestCase):

    def test_model(self):
        assert self.night_rate_range

    def test_get_night_rate_ok(self):
        assert get_night_rate(timezone.datetime.today())


class TestApartmentRental(CustomTestCase):

    def test_nights(self):
        self.assertEqual(self.apartment_rental.nights, 7)

    def test_description_short(self):
        assert self.apartment_rental.description_short

    def test_description_long(self):
        assert self.apartment_rental.description_long

    def test_type(self):
        assert self.apartment_rental.type

    def test_url(self):
        assert self.apartment_rental.url



