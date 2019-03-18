from django.apps import apps
from clickgestion.core.test import CustomTestCase, CustomModelTestCase
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


class TestCashFloatDepositModel(CustomTestCase, CustomModelTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_attrs = [
            '_code_initials',
            '_concept_class',
            '_settings_class',
            '_url',
            '_verbose_name',
            '__str__',
            'description_short',
            'name',
        ]
        model = model_creation.create_test_cash_float_deposit(
            model_creation.create_test_transaction(cls.admin, timezone.now()), timezone.now())
        cls.model_object = model


class TestCashFloatWithdrawalModel(CustomTestCase, CustomModelTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_attrs = [
            '_code_initials',
            '_concept_class',
            '_settings_class',
            '_url',
            '_verbose_name',
            '__str__',
            'description_short',
            'name',
        ]
        model = model_creation.create_test_cash_float_withdrawal(
            model_creation.create_test_transaction(cls.admin, timezone.now()), timezone.now())
        cls.model_object = model
