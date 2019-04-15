from clickgestion.service_sales.models import Service, ServiceSale
from clickgestion.core.test import CustomTestCase, CustomModelTestCase
from clickgestion.concepts.test_models import BaseConceptModelTest
from clickgestion.core import model_creation
from django.utils import timezone


class TestService(CustomTestCase, CustomModelTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_attrs = [
            '__str__',
            'per_transaction',
        ]
        cls.model_object = cls.service


class TestServiceSale(BaseConceptModelTest):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_object = cls.ticketsale

    def test_all_sale_descriptions(self):
        service = model_creation.create_service(
            model_creation.create_servicecompany('Test Inc.'),
            'Test Service 1',
            date_required=True,
            per_adult=True,
            per_child=True,
            per_night=True,
            per_senior=True,
            per_unit=True,
            variable_price=True,
        )
        service = model_creation.create_service(
            model_creation.create_servicecompany('Test Inc.'),
            'Test Service 2',
            date_required=True,
            per_adult=False,
            per_child=False,
            per_night=True,
            per_senior=False,
            per_unit=False,
            variable_price=True,
        )
        for service in Service.objects.all():
            transaction = model_creation.create_test_transaction(self.admin, timezone.now())
            ticketsale = model_creation.create_test_ticketsale(transaction, timezone.now(), service=service)
            message = 'Testing description for ServiceSale {}: {}'.format(ticketsale.id, ticketsale)
            self.assertTrue(ticketsale.description_short, msg=message)
