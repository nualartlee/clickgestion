from clickgestion.ticket_sales.models import Show, TicketSale
from clickgestion.core.test import CustomTestCase, CustomModelTestCase
from clickgestion.concepts.test_models import BaseConceptModelTest
from django.utils import timezone


class TestShow(CustomTestCase, CustomModelTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_attrs = [
            '__str__',
            'per_transaction',
        ]
        cls.model_object = cls.show


class TestTicketSale(BaseConceptModelTest):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_object = cls.ticketsale
