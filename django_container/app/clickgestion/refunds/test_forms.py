from clickgestion.core.test import CustomTestCase
from clickgestion.refunds import forms
from django.utils import timezone
from clickgestion.core import model_creation
from django.apps import apps


class RefundFormTest(CustomTestCase):

    form_class = forms.RefundForm

    def test_form_ok(self):
        transaction1 = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction1, timezone.now())
        transaction1.close(self.admin)
        transaction2 = model_creation.create_test_transaction(self.admin, timezone.now())
        value = apps.get_model('concepts.conceptvalue')(
            amount=aptrental.value.amount,
            currency=aptrental.value.currency,
            credit=False,
        )
        value.save()
        form_data = {
            'transaction': transaction2.id,
            'value': value.id,
            'vat_percent': aptrental.vat_percent,
            'refunded_concept': aptrental.id,
        }
        form = self.form_class(data=form_data)
        self.assertTrue(form.is_valid())
