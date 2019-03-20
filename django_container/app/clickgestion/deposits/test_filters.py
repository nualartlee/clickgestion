from clickgestion.core.test import CustomTestCase
from clickgestion.deposits.filters import DepositFilter
from clickgestion.core import model_creation
from django.utils import timezone


class DepositFilterTest(CustomTestCase):

    def test_returned(self):

        # None returned
        filter_data = {
            'returned': True,
        }
        deposit_filter = DepositFilter(data=filter_data)
        self.assertFalse(deposit_filter.qs)

        # One returned
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        aptrentaldeposit = model_creation.create_test_aptrentaldeposit(transaction, aptrental, timezone.now())
        transaction.close(self.admin)
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        depositreturn = model_creation.create_test_depositreturn(transaction, aptrentaldeposit, timezone.now())
        transaction.close(self.admin)
        deposit_filter = DepositFilter(data=filter_data)
        self.assertTrue(deposit_filter.qs)


