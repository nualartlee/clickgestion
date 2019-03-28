"""
For future use

from clickgestion.core.test import CustomTestCase
from clickgestion.deposits.filters import DepositFilter
from clickgestion.core import model_creation
from django.utils import timezone


class DepositFilterTest(CustomTestCase):

    def test_returned_filter(self):

        # Initial returned
        filter_data = {
            'returned': True,
        }
        deposit_filter = DepositFilter(data=filter_data)
        initial_returned = deposit_filter.qs.count()

        # One more returned
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        aptrentaldeposit = model_creation.create_test_aptrentaldeposit(transaction, aptrental, timezone.now())
        transaction.close(self.admin)
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        depositreturn = model_creation.create_test_depositreturn(transaction, aptrentaldeposit, timezone.now())
        transaction.close(self.admin)
        deposit_filter = DepositFilter(data=filter_data)
        self.assertEqual(deposit_filter.qs.count(), initial_returned + 1)

        # Initial pending
        filter_data = {
            'returned': False,
        }
        deposit_filter = DepositFilter(data=filter_data)
        initial_pending = deposit_filter.qs.count()

        # One more pending
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        aptrentaldeposit = model_creation.create_test_aptrentaldeposit(transaction, aptrental, timezone.now())
        transaction.close(self.admin)
        deposit_filter = DepositFilter(data=filter_data)
        self.assertEqual(deposit_filter.qs.count(), initial_pending + 1)

"""

