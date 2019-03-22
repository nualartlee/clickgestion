from clickgestion.core.test import CustomTestCase
from clickgestion.core import model_creation
from django.utils import timezone


class ModelCreationTest(CustomTestCase):

    def test_create_test_models(self):
        self.assertIsNone(model_creation.create_test_models(days=2))

    def test_create_one_of_each(self):
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        aptrentaldeposit = model_creation.create_test_aptrentaldeposit(transaction, aptrental, timezone.now())
        transaction.close(self.admin)
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        cashfloatdeposit = model_creation.create_test_cashfloatdeposit(transaction, timezone.now())
        cashfloatwithdrawal = model_creation.create_test_cashfloatwithdrawal(transaction, timezone.now())
        transaction.close(self.admin)
        cashclose = model_creation.create_test_cashclose(timezone.now(), self.admin)
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        depositreturn = model_creation.create_test_depositreturn(transaction, aptrentaldeposit, timezone.now())
        refund = model_creation.create_test_refund(transaction, aptrental, timezone.now())
