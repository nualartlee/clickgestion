from clickgestion.core.test import CustomTestCase
from clickgestion.transactions.models import Transaction, get_new_transaction_code


class TestGetNewTransactionID(CustomTestCase):

    def test_get_new_transaction_code(self):
        code = get_new_transaction_code()
        assert code


class TestTransaction(CustomTestCase):

    def test_unicode(self):
        assert self.transaction.__unicode__()

    def test_client(self):
        assert self.transaction.client

    def test_description_short(self):
        assert self.transaction.description_short

    def test_total(self):
        assert self.transaction.total


