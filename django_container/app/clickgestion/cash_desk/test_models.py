from django.apps import apps
from clickgestion.core.test import CustomTestCase, CustomModelTestCase
from clickgestion.concepts.test_models import BaseConceptModelTest
from clickgestion.cash_desk.models import get_new_cashclose_code
from clickgestion.core import model_creation
from django.utils import timezone


class TestGetNewCashCloseCode(CustomTestCase):

    def test_get_new_cashclose_code(self):
        code = get_new_cashclose_code()
        assert code


class TestCashCloseModel(CustomTestCase, CustomModelTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_attrs = [
            '__str__',
            'code',
            'created',
            'employee',
            'notes',
            'updated',
            'balance',
            'breakdown_by_accounting_group',
            'breakdown_by_concept_type',
            'breakdowns',
            'concepts',
        ]
        model_creation.create_test_models(days=3)
        cls.model_object = apps.get_model('cash_desk.CashClose').objects.first()

    def test_save_again(self):
        self.assertEqual(self.model_object.save(), None)


class TestCashFloatDepositModel(BaseConceptModelTest):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        model = model_creation.create_test_cashfloatdeposit(
            model_creation.create_test_transaction(cls.admin, timezone.now()), timezone.now())
        cls.model_object = model


class TestCashFloatWithdrawalModel(BaseConceptModelTest):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        model = model_creation.create_test_cashfloatwithdrawal(
            model_creation.create_test_transaction(cls.admin, timezone.now()), timezone.now())
        cls.model_object = model
