from clickgestion.core.test import CustomTestCase
from clickgestion.core import model_creation
from django.utils import timezone
from clickgestion.transactions.forms import TransactionEditForm, TransactionPayForm
from django.forms.models import model_to_dict


class TransactionEditFormTest(CustomTestCase):
    form_type = TransactionEditForm

    def test_form_ok(self):
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        form = self.form_type(model_to_dict(transaction), instance=transaction)
        self.assertTrue(form.is_valid())

    def test_form_no_concepts(self):
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        form = self.form_type(model_to_dict(transaction), instance=transaction)
        self.assertFalse(form.is_valid())
        self.assertIn('No concepts.', form.non_field_errors())


class TransactionPayFormTest(CustomTestCase):
    form_type = TransactionPayForm

    def test_form_ok(self):
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        form = self.form_type(model_to_dict(transaction), instance=transaction)
        self.assertTrue(form.is_valid())
