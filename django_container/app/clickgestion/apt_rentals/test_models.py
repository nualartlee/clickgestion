from clickgestion.apt_rentals.models import AptRental, NightRateRange, get_night_rate
from clickgestion.core.test import CustomTestCase, CustomModelTestCase
from django.utils import timezone


class TestNightRateRange(CustomTestCase, CustomModelTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_attrs = [
            '__str__',
        ]
        cls.model_object = cls.nightraterange

    def test_get_night_rate_ok(self):
        assert get_night_rate(timezone.datetime.today())


class TestAptRental(CustomTestCase, CustomModelTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_attrs = [
            '__str__',
            '_url',
            '_code_initials',
            '_concept_class',
            '_settings_class',
            '_verbose_name',
            'description_short',
            'get_current_rates',
            'get_value',
            'name',
            'nights',
        ]
        cls.model_object = cls.aptrental
