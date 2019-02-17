from clickgestion.core.test import CustomTestCase
from clickgestion.transactions.models import Transaction, get_new_transaction_code


class TestGetNewTransactionID(CustomTestCase):

    def test_get_new_transaction_code(self):
        code = get_new_transaction_code()
        assert code


class TestTransaction(CustomTestCase):

    def test_str(self):
        assert self.transaction.__str__()

    def test_client(self):
        self.assertEqual(self.transaction.client, '')
        self.transaction.client_first_name = 'Bob'
        self.assertEqual(self.transaction.client, 'Bob')
        self.transaction.client_last_name = 'Smith'
        self.assertEqual(self.transaction.client, 'Bob Smith')
        self.transaction.client_first_name = ''
        self.assertEqual(self.transaction.client, 'Smith')

    def test_description_short(self):
        assert self.transaction.description_short

    def test_totals(self):
        assert self.transaction.totals


