from clickgestion.service_sales.models import Service
from clickgestion.core.test import CustomTestCase, CustomModelTestCase
from clickgestion.concepts.test_models import ConceptModelTest
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


class TestServiceSale(ConceptModelTest):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_object = cls.servicesale

    def test_all_sale_descriptions(self):
        service = model_creation.create_service(
            model_creation.create_servicetype('Test Inc.'),
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
            model_creation.create_servicetype('Test Inc.'),
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
            servicesale = model_creation.create_test_servicesale(transaction, timezone.now(),
                                                                 service=service,
                                                                 adults=1,
                                                                 children=1,
                                                                 seniors=1,
                                                                 units=1)
            servicesale2 = model_creation.create_test_servicesale(transaction, timezone.now(),
                                                                 service=service,
                                                                 adults=2,
                                                                 children=2,
                                                                 seniors=2,
                                                                 units=2)
            message = 'Testing description for ServiceSale {}: {}'.format(servicesale.id, servicesale)
            self.assertTrue(servicesale.description_short, msg=message)
            self.assertTrue(servicesale2.description_short, msg=message)

    def test_closed_transaction(self):
        self.servicesale.transaction.close(self.admin)
        self.test_get_value()

