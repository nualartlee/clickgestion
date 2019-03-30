from clickgestion.core.test import CustomTestCase
from clickgestion.transactions.filters import TransactionFilter


class TestTransactionFilter(CustomTestCase):

    def test_filter_ok(self):

        # Initial returned
        filter_data = {
        }
        self.assertTrue(TransactionFilter(data=filter_data))
