from clickgestion.core.test import CustomTestCase, CustomModelTestCase
from clickgestion.refunds.models import Refund
from clickgestion.core import model_creation
from django.utils import timezone


class RefundTest(CustomTestCase, CustomModelTestCase):

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
            'get_value',
            'name',
            'refunded_concept'
        ]
        cls.model_object = Refund(transaction=cls.transaction, refunded_concept=cls.aptrentaldeposit)
