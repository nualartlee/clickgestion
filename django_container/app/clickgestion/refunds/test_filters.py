from clickgestion.core.test import CustomTestCase
from clickgestion.refunds.filters import RefundFilter
from clickgestion.core import model_creation
from django.utils import timezone


class RefundFilterTest(CustomTestCase):

    def test_returned_filter(self):

        # Initial refunded
        filter_data = {
        }
        filter = RefundFilter(data=filter_data)
        initial_refunded = filter.qs.count()

        # One more refunded
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        transaction.close(self.admin)
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        refund = model_creation.create_test_refund(transaction, aptrental, timezone.now())
        transaction.close(self.admin)
        filter = RefundFilter(data=filter_data)
        self.assertEqual(filter.qs.count(), initial_refunded + 1)
