from clickgestion.concepts.models import BaseConcept
from clickgestion.core.test import CustomTestCase, CustomModelTestCase
from clickgestion.refunds.models import Refund
from clickgestion.core import model_creation
from django.utils import timezone
from django.core.exceptions import FieldError


class RefundTest(CustomTestCase, CustomModelTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_attrs = [
            '__str__',
            '_url',
            '_code_initials',
            '_concept_class',
            '_settings_class',
            '_verbose_name',
            'description_short',
            'get_value',
            'name',
            'refunded_concept'
        ]
        cls.model_object = Refund(transaction=cls.transaction, refunded_concept=cls.aptrentaldeposit)

    def test_save(self):
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        transaction.close(self.admin)
        self.assertFalse(aptrental.refund_concept)
        self.assertTrue(aptrental.can_refund)
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        refund = model_creation.create_test_refund(
            transaction, aptrental, timezone.now())
        self.assertFalse(aptrental.refund_concept)
        self.assertTrue(aptrental.can_refund)
        transaction.close(self.admin)
        self.assertTrue(aptrental.refund_concept)
        self.assertFalse(aptrental.can_refund)
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        with self.assertRaises(FieldError):
            model_creation.create_test_refund(transaction, aptrental, timezone.now())

    def test_refunded_concept(self):
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        transaction.close(self.admin)
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        refund = model_creation.create_test_refund(
            transaction, aptrental, timezone.now())
        transaction.close(self.admin)
        baserefund = BaseConcept.objects.get(code=refund.code)
        self.assertTrue(baserefund.refunded_concept)

