from clickgestion.core.test import CustomTestCase
from clickgestion.concepts.forms import ConceptValueForm
from django.apps import apps


class ConceptValueFormTest(CustomTestCase):

    form_class = ConceptValueForm

    def test_form_ok(self):
        form_data = {
            'currency': apps.get_model('concepts.Currency').objects.first().id,
            'amount': 200,
        }
        form = self.form_class(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_missing_currency(self):
        form_data = {
            'amount': 200,
        }
        form = self.form_class(data=form_data)
        self.assertIn('This field is required.', form.errors['currency'])
        self.assertFalse(form.is_valid())

    def test_form_missing_amount(self):
        form_data = {
            'currency': apps.get_model('concepts.Currency').objects.first().id,
        }
        form = self.form_class(data=form_data)
        self.assertIn('This field is required.', form.errors['amount'])
        self.assertFalse(form.is_valid())

    def test_form_negative_amount(self):
        form_data = {
            'currency': apps.get_model('concepts.Currency').objects.first().id,
            'amount': -200,
        }
        form = self.form_class(data=form_data)
        self.assertIn('Enter a positive amount.', form.errors['amount'])
        self.assertFalse(form.is_valid())

    def test_form_bad_amount(self):
        form_data = {
            'currency': apps.get_model('concepts.Currency').objects.first().id,
            'amount': 'f200',
        }
        form = self.form_class(data=form_data)
        self.assertIn('Enter a number.', form.errors['amount'])
        self.assertFalse(form.is_valid())
