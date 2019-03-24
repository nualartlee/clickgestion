from clickgestion.core.test import CustomTestCase
from clickgestion.transactions.filters import TransactionFilter
from clickgestion.core import model_creation
from django.utils import timezone


class TestTransactionFilter(CustomTestCase):

    def test_filter_ok(self):

        # Initial returned
        filter_data = {
        }
        filter = TransactionFilter(data=filter_data)
        #import pdb;pdb.set_trace()
