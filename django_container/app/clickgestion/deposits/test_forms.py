from clickgestion.core.test import CustomTestCase
from clickgestion.deposits import forms
from django.utils import timezone
from clickgestion.core import model_creation
from django.apps import apps


class AptRentalDepositFormTest(CustomTestCase):

    form_class = forms.AptRentalDepositForm

    def test_form_ok(self):
        form_data = {
            'adults': 2,
            'children': 1,
            'end_date': timezone.now() + timezone.timedelta(days=10),
            'start_date': timezone.now() + timezone.timedelta(days=3),
        }
        form = self.form_class(data=form_data)
        self.assertTrue(form.is_valid())


class DepositReturnFormTest(CustomTestCase):

    form_class = forms.DepositReturnForm

    def test_form_ok(self):
        transaction1 = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction1, timezone.now())
        aptrentaldeposit = model_creation.create_test_aptrentaldeposit(transaction1, aptrental, timezone.now())
        transaction1.close(self.admin)
        transaction2 = model_creation.create_test_transaction(self.admin, timezone.now())
        value = apps.get_model('concepts.conceptvalue')(
            amount=aptrentaldeposit.value.amount,
            currency=aptrentaldeposit.value.currency,
            credit=False,
        )
        value.save()
        form_data = {
            'transaction': transaction2.id,
            'value': value.id,
            'vat_percent': 0,
            'returned_deposit': aptrentaldeposit.id,
        }
        form = self.form_class(data=form_data)
        self.assertTrue(form.is_valid())
