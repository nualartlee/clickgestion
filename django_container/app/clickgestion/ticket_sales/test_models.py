from clickgestion.ticket_sales.models import Show
from clickgestion.core.test import CustomTestCase, CustomModelTestCase
from clickgestion.concepts.test_models import ConceptModelTest
from clickgestion.core import model_creation
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


class TestTicketSale(ConceptModelTest):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_object = cls.ticketsale

    def test_all_sale_descriptions(self):
        show = model_creation.create_show(
            model_creation.create_showcompany('Test Inc.'),
            'Test Show 1',
            date_required=True,
            per_adult=True,
            per_child=True,
            per_night=True,
            per_senior=True,
            per_unit=True,
            variable_price=True,
        )
        show = model_creation.create_show(
            model_creation.create_showcompany('Test Inc.'),
            'Test Show 2',
            date_required=True,
            per_adult=False,
            per_child=False,
            per_night=True,
            per_senior=False,
            per_unit=False,
            variable_price=True,
        )
        for show in Show.objects.all():
            transaction = model_creation.create_test_transaction(self.admin, timezone.now())
            ticketsale = model_creation.create_test_ticketsale(transaction, timezone.now(), show=show)
            message = 'Testing description for TicketSale {}: {}'.format(ticketsale.id, ticketsale)
            self.assertTrue(ticketsale.description_short, msg=message)
