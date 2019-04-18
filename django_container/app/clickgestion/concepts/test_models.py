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
            'can_refund',
            'can_return_deposit',
            'child',
            'code',
            'concept_class',
            'concept_name',
            'created',
            'department',
            'deposit_return',
            'description_short',
            'end_date',
            'is_child',
            'name',
            'name_plural',
            'refund_concept',
            'refunded_concept',
            'returned_deposit',
            'save',
            'settings',
            'start_date',
            'tax_amount',
            'taxable_amount',
            'transaction',
            'updated',
            'url',
            'value',
            'vat_percent',
        ]

    def test_get_all_permissions(self):
        if not self.model_object:
            return
        self.assertTrue(self.model_object.get_all_permissions())

    def test_get_value(self):
        if not self.model_object:
            return
        self.assertTrue(self.model_object.get_value())

    def test_with_closed_transaction(self):
        if not self.model_object:
            return
        self.model_object.transaction.close(self.admin)
        self.test_attrs()
        self.test_get_value()


class ConceptModelTest(BaseConceptModelTest):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_object = BaseConcept.objects.first()

    def test_get_all_permissions(self):
        self.assertTrue(self.model_object.get_all_permissions())

    def test_get_value(self):
        self.assertTrue(self.model_object.get_value())

    def test_deposit_returned(self):
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        aptrentaldeposit = model_creation.create_test_aptrentaldeposit(transaction, aptrental, timezone.now())
        aptrentaldepositbase = BaseConcept.objects.get(code=aptrentaldeposit.code)
        transaction.close(self.admin)
        self.assertFalse(aptrentaldeposit.deposit_return)
        self.assertTrue(aptrentaldeposit.can_return_deposit)
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        depositreturn = model_creation.create_test_depositreturn(
            transaction, aptrentaldeposit, timezone.now())
        depositreturnbase = BaseConcept.objects.get(code=depositreturn.code)
        self.assertFalse(aptrentaldeposit.deposit_return)
        self.assertFalse(aptrentaldepositbase.deposit_return)
        self.assertTrue(aptrentaldeposit.can_return_deposit)
        self.assertTrue(aptrentaldepositbase.can_return_deposit)
        transaction.close(self.admin)
        self.assertTrue(aptrentaldeposit.deposit_return)
        self.assertTrue(aptrentaldepositbase.deposit_return)
        self.assertTrue(depositreturn.returned_deposit)
        self.assertTrue(depositreturnbase.returned_deposit)
        self.assertFalse(aptrentaldeposit.can_return_deposit)
        self.assertFalse(aptrentaldepositbase.can_return_deposit)

    def test_refunded(self):
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        aptrentalbase = BaseConcept.objects.get(code=aptrental.code)
        transaction.close(self.admin)
        self.assertFalse(aptrental.refund_concept)
        self.assertFalse(aptrentalbase.refund_concept)
        self.assertTrue(aptrental.can_refund)
        self.assertTrue(aptrentalbase.can_refund)
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        refund = model_creation.create_test_refund(
            transaction, aptrental, timezone.now())
        refundbase = BaseConcept.objects.get(code=refund.code)
        self.assertFalse(aptrental.refund_concept)
        self.assertFalse(aptrentalbase.refund_concept)
        self.assertTrue(aptrentalbase.can_refund)
        transaction.close(self.admin)
        self.assertTrue(aptrental.refund_concept)
        self.assertTrue(aptrentalbase.refund_concept)
        self.assertTrue(refund.refunded_concept)
        self.assertTrue(refundbase.refunded_concept)
        self.assertFalse(aptrental.can_refund)
        self.assertFalse(aptrentalbase.can_refund)

    def test_tax_amount(self):
        self.assertEqual(0, self.aptrentaldeposit.tax_amount)


class SingletonModelTest(CustomTestCase):

    def test_load(self):
        self.aptrentaldeposit.settings.load()
