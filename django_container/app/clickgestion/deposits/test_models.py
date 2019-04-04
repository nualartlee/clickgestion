from clickgestion.deposits.models import AptRentalDeposit, DepositReturn, ParkingRentalDeposit, SafeRentalDeposit
from clickgestion.concepts.models import BaseConcept
from clickgestion.concepts.test_models import BaseConceptModelTest
from django.core.exceptions import FieldError
from clickgestion.core import model_creation
from django.utils import timezone


class AptRentalDepositTest(BaseConceptModelTest):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
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


class DepositReturnTest(BaseConceptModelTest):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.aptrentaldeposit.transaction.close(cls.admin)
        model = DepositReturn(transaction=cls.transaction, returned_deposit=cls.aptrentaldeposit)
        model.save()
        cls.model_object = model

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
        with self.assertRaises(FieldError):
            model_creation.create_test_depositreturn(transaction, aptrentaldeposit, timezone.now())

    def test_returned_deposit(self):
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        aptrentaldeposit = model_creation.create_test_aptrentaldeposit(transaction, aptrental, timezone.now())
        transaction.close(self.admin)
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        deposit_return = model_creation.create_test_depositreturn(
            transaction, aptrentaldeposit, timezone.now())
        basereturn = BaseConcept.objects.get(code=deposit_return.code)
        self.assertTrue(basereturn.returned_deposit)


class ParkingRentalDepositTest(BaseConceptModelTest):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_object = cls.parkingrentaldeposit

    def test_save_with_parkingrental(self):
        transaction1 = model_creation.create_test_transaction(self.admin, timezone.now())
        parkingrental = model_creation.create_test_parkingrental(transaction1, timezone.now())
        self.assertIsNone(ParkingRentalDeposit().save(parkingrental=parkingrental))


class SafeRentalDepositTest(BaseConceptModelTest):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_object = cls.saferentaldeposit

    def test_save_with_saferental(self):
        transaction1 = model_creation.create_test_transaction(self.admin, timezone.now())
        saferental = model_creation.create_test_saferental(transaction1, timezone.now())
        self.assertIsNone(SafeRentalDeposit().save(saferental=saferental))
