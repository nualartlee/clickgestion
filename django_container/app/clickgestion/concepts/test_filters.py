from clickgestion.core.test import CustomTestCase
from clickgestion.concepts.filters import ConceptFilter
from clickgestion.core import model_creation
from django.utils import timezone


class TestConceptFilter(CustomTestCase):

    def test_filter_ok(self):

        # Initial returned
        filter_data = {
        }
        filter = ConceptFilter(data=filter_data)

    def test_deposit_status_filter(self):

        # Initial returned
        filter_data = {
            'deposit_status': True,
        }
        concept_filter = ConceptFilter(data=filter_data)
        initial_returned = concept_filter.qs.count()

        # One more returned
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        aptrentaldeposit = model_creation.create_test_aptrentaldeposit(transaction, aptrental, timezone.now())
        transaction.close(self.admin)
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        depositreturn = model_creation.create_test_depositreturn(transaction, aptrentaldeposit, timezone.now())
        transaction.close(self.admin)
        concept_filter = ConceptFilter(data=filter_data)
        self.assertEqual(concept_filter.qs.count(), initial_returned + 1)

        # Initial pending
        filter_data = {
            'deposit_status': False,
        }
        concept_filter = ConceptFilter(data=filter_data)
        initial_pending = concept_filter.qs.count()

        # One more pending
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        aptrentaldeposit = model_creation.create_test_aptrentaldeposit(transaction, aptrental, timezone.now())
        transaction.close(self.admin)
        concept_filter = ConceptFilter(data=filter_data)
        self.assertEqual(concept_filter.qs.count(), initial_pending + 1)

    def test_refund_status_filter(self):

        # Initial refunded
        filter_data = {
            'refund_status': True,
        }
        concept_filter = ConceptFilter(data=filter_data)
        initial_refunded = concept_filter.qs.count()

        # One more refunded
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        transaction.close(self.admin)
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        refund = model_creation.create_test_refund(transaction, aptrental, timezone.now())
        transaction.close(self.admin)
        concept_filter = ConceptFilter(data=filter_data)
        self.assertEqual(concept_filter.qs.count(), initial_refunded + 1)

        # Initial pending
        filter_data = {
            'refund_status': False,
        }
        concept_filter = ConceptFilter(data=filter_data)
        initial_pending = concept_filter.qs.count()

        # One more pending
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        transaction.close(self.admin)
        concept_filter = ConceptFilter(data=filter_data)
        self.assertEqual(concept_filter.qs.count(), initial_pending + 1)
