from clickgestion.core.test import CustomTestCase, CustomModelTestCase
from clickgestion.transactions.models import get_new_transaction_code
from clickgestion.core import model_creation
from django.utils import timezone


class TestGetNewTransactionID(CustomTestCase):

    def test_get_new_transaction_code(self):
        code = get_new_transaction_code()
        assert code


class TestTransaction(CustomTestCase, CustomModelTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_attrs = [
            '__str__',
            'description_short',
            'totals',
            'client_signature_required',
            'employee_signature_required',
            'title',
        ]
        cls.model_object = cls.transaction

    def test_client(self):
        self.assertEqual(self.transaction.client, '')
        self.transaction.client_first_name = 'Bob'
        self.assertEqual(self.transaction.client, 'Bob')
        self.transaction.client_last_name = 'Smith'
        self.assertEqual(self.transaction.client, 'Bob Smith')
        self.transaction.client_first_name = ''
        self.assertEqual(self.transaction.client, 'Smith')

    def test_client_signature_required(self):

        # Not required
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        self.assertFalse(transaction.client_signature_required)

        # Required
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        aptrentaldeposit = model_creation.create_test_aptrentaldeposit(transaction, aptrental, timezone.now())
        transaction.close(self.admin)
        transaction2 = model_creation.create_test_transaction(self.admin, timezone.now())
        depositreturn = model_creation.create_test_depositreturn(transaction2, aptrentaldeposit, timezone.now())
        transaction2.close(self.admin)
        self.assertTrue(transaction2.client_signature_required)

    def test_closed(self):
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        aptrentaldeposit = model_creation.create_test_aptrentaldeposit(transaction, aptrental, timezone.now())
        transaction.close(self.admin)
        timestamp = transaction.closed_date
        transaction.close(self.admin)
        self.assertEqual(timestamp, transaction.closed_date)

    def test_employee_signature_required(self):

        # Not required
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        self.assertFalse(transaction.employee_signature_required)

        # Required
        cashfloatdeposit = model_creation.create_test_cashfloatdeposit(transaction, timezone.now())
        settings = cashfloatdeposit.settings
        settings.employee_signature_required = True
        settings.save()
        self.assertTrue(transaction.employee_signature_required)

    def test_empty(self):
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        self.model_object = transaction
        self.test_attrs()

    def test_title(self):
        self.assertTrue(self.transaction.title)

    def test_with_cash(self):
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        cashfloatdeposit = model_creation.create_test_cashfloatdeposit(transaction, timezone.now())
        transaction.apt_number = 1008
        transaction.client_first_name = 'Donna'
        transaction.client_last_name = 'Kavanagh'
        transaction.close(self.admin)
        self.model_object = transaction
        self.test_attrs()

    def test_with_return(self):
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        aptrentaldeposit = model_creation.create_test_aptrentaldeposit(transaction, aptrental, timezone.now())
        transaction.close(self.admin)
        transaction2 = model_creation.create_test_transaction(self.admin, timezone.now())
        depositreturn = model_creation.create_test_depositreturn(transaction2, aptrentaldeposit, timezone.now())
        transaction2.close(self.admin)
        self.model_object = transaction2
        self.test_attrs()



