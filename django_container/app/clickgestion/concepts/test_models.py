from clickgestion.core.test import CustomTestCase, CustomModelTestCase
from clickgestion.concepts.models import BaseConcept, Currency, ConceptValue
from clickgestion.core import model_creation
from django.utils import timezone


class CurrencyModelTest(CustomTestCase, CustomModelTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_attrs = [
            'name',
            'code_a',
            'code_n',
            'enabled',
            'default',
            'exchange_rate',
            'symbol',
            '__str__',
        ]
        cls.model_object = Currency.objects.first()


class ConceptValueModelTest(CustomTestCase, CustomModelTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_attrs = [
            'amount',
            'created',
            'credit',
            'currency',
            'updated',
            '__str__',
        ]
        cls.model_object = ConceptValue.objects.first()


class BaseConceptModelTest(CustomTestCase, CustomModelTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_attrs = [
            'accounting_group',
            'code',
            'concept_class',
            'concept_name',
            'created',
            'end_date',
            'start_date',
            'transaction',
            'updated',
            'value',
            'vat_percent',
            'can_return_deposit',
            'child',
            'deposit_returned',
            'description_short',
            'is_child',
            'name',
            'name_plural',
            'save',
            'settings',
            'tax_amount',
            'taxable_amount',
            'url',
        ]
        cls.model_object = BaseConcept.objects.first()

    def test_get_all_permissions(self):
        self.assertTrue(self.model_object.get_all_permissions())

    def test_get_value(self):
        self.assertTrue(self.model_object.get_value())

    def test_deposit_returned(self):
        self.assertFalse(self.aptrentaldeposit.deposit_return)
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        deposit_return = model_creation.create_test_depositreturn(
            transaction, self.aptrentaldeposit, timezone.now())
        self.assertFalse(self.aptrentaldeposit.deposit_return)
        transaction.closed = True
        transaction.save()
        self.assertTrue(self.aptrentaldeposit.deposit_return)

    def test_tax_amount(self):
        self.assertEqual(0, self.aptrentaldeposit.tax_amount)


class SingletonModelTest(CustomTestCase):

    def test_load(self):
        self.aptrentaldeposit.settings.load()
