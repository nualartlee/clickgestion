from clickgestion.core.test import CustomTestCase, CustomModelTestCase
from clickgestion.concepts.models import BaseConcept


class TestBaseConcept(CustomTestCase, CustomModelTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_attrs = [
            '__str__',
            'description_short',
        ]
        cls.model_object = cls.apartment_rental


