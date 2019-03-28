from clickgestion.apt_rentals.models import AptRental, NightRateRange, get_night_rate
from clickgestion.core.test import CustomTestCase, CustomModelTestCase
from clickgestion.concepts.test_models import BaseConceptModelTest
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


class TestAptRental(BaseConceptModelTest):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_object = cls.aptrental
