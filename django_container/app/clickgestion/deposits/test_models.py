from clickgestion.core.test import CustomTestCase, CustomModelTestCase
from clickgestion.deposits.models import AptRentalDeposit, DepositReturn
from clickgestion.core import model_creation
from django.utils import timezone
from django.core.exceptions import FieldError


class DepositReturnTest(CustomTestCase, CustomModelTestCase):

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
        ]
        cls.model_object = DepositReturn(transaction=cls.transaction, returned_deposit=cls.aptrentaldeposit)

    def test_save(self):
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        aptrentaldeposit = model_creation.create_test_aptrentaldeposit(transaction, aptrental, timezone.now())
        transaction.close(self.admin)
        self.assertFalse(aptrentaldeposit.deposit_return)
        self.assertTrue(aptrentaldeposit.can_return_deposit)
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        deposit_return = model_creation.create_test_depositreturn(
            transaction, aptrentaldeposit, timezone.now())
        self.assertFalse(aptrentaldeposit.deposit_return)
        self.assertTrue(aptrentaldeposit.can_return_deposit)
        transaction.close(self.admin)
        self.assertTrue(aptrentaldeposit.deposit_return)
        self.assertFalse(aptrentaldeposit.can_return_deposit)
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        deposit_return = model_creation.create_test_depositreturn(
            transaction, aptrentaldeposit, timezone.now())
        self.assertRaises(
            FieldError, model_creation.create_test_depositreturn(transaction, aptrentaldeposit, timezone.now()))


class AptRentalDepositTest(CustomTestCase, CustomModelTestCase):

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
            'nights',
        ]
        cls.model_object = cls.aptrentaldeposit

    def test_save_with_aptrental(self):
        transaction1 = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction1, timezone.now())
        self.assertIsNone(AptRentalDeposit().save(aptrental=aptrental))

    def test_max_value(self):
        transaction1 = model_creation.create_test_transaction(self.admin, timezone.now())
        start_date = timezone.now()
        aptrental = model_creation.create_test_aptrental(
            transaction1, timezone.now(),
            adults=4,
            children=0,
            end_date=start_date + timezone.timedelta(days=100),
            start_date=start_date,
        )
        aptrentaldeposit = AptRentalDeposit()
        aptrentaldeposit.save(aptrental=aptrental)
        self.assertEqual(aptrentaldeposit.value.amount, aptrentaldeposit.settings.max)

    def test_min_value(self):
        transaction1 = model_creation.create_test_transaction(self.admin, timezone.now())
        start_date = timezone.now()
        aptrental = model_creation.create_test_aptrental(
            transaction1, timezone.now(),
            adults=1,
            children=0,
            end_date=start_date + timezone.timedelta(days=1),
            start_date=start_date,
        )
        aptrentaldeposit = AptRentalDeposit()
        aptrentaldeposit.save(aptrental=aptrental)
        self.assertEqual(aptrentaldeposit.value.amount, aptrentaldeposit.settings.min)


