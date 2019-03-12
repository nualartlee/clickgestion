from clickgestion.core.test import CustomTestCase, CustomModelTestCase
from clickgestion.transactions.models import get_new_transaction_code


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


