from clickgestion.core.test import CustomTestCase
from clickgestion.cash_desk.forms import CashCloseForm, CashFloatDepositForm, CashFloatWithdrawalForm
from django.apps import apps


class CashCloseFormTest(CustomTestCase):

    def test_form_ok(self):
        form_data = {
        }
        form = CashCloseForm(data=form_data)
        self.assertTrue(form.is_valid())


class CashFloatDepositFormTest(CustomTestCase):

    def test_form_ok(self):
        form_data = {
            'currency': apps.get_model('concepts.Currency').objects.first().id,
            'amount': 200,
        }
        form = CashFloatDepositForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_missing_currency(self):
        form_data = {
            'amount': 200,
        }
        form = CashFloatDepositForm(data=form_data)
        self.assertIn('This field is required.', form.errors['currency'])
        self.assertFalse(form.is_valid())

    def test_form_missing_amount(self):
        form_data = {
            'currency': apps.get_model('concepts.Currency').objects.first().id,
        }
        form = CashFloatDepositForm(data=form_data)
        self.assertIn('This field is required.', form.errors['amount'])
        self.assertFalse(form.is_valid())

    def test_form_negative_amount(self):
        form_data = {
            'currency': apps.get_model('concepts.Currency').objects.first().id,
            'amount': -200,
        }
        form = CashFloatDepositForm(data=form_data)
        self.assertIn('Enter a positive amount.', form.errors['amount'])
        self.assertFalse(form.is_valid())

    def test_form_bad_amount(self):
        form_data = {
            'currency': apps.get_model('concepts.Currency').objects.first().id,
            'amount': 'f200',
        }
        form = CashFloatDepositForm(data=form_data)
        self.assertIn('Enter a number.', form.errors['amount'])
        self.assertFalse(form.is_valid())

    def test_form_save(self):
        form_data = {
            'currency': apps.get_model('concepts.Currency').objects.first().id,
            'amount': 200,
        }
        form = CashFloatDepositForm(data=form_data)
        transaction = apps.get_model('transactions.Transaction')(employee=self.admin)
        transaction.save()
        form.instance.transaction = transaction
        self.assertTrue(form.is_valid())
        instance = form.save()
        self.assertTrue(instance)


class CashFloatWithdrawalFormTest(CustomTestCase):

    def test_form_ok(self):
        form_data = {
            'currency': apps.get_model('concepts.Currency').objects.first().id,
            'amount': 200,
        }
        form = CashFloatWithdrawalForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_missing_currency(self):
        form_data = {
            'amount': 200,
        }
        form = CashFloatWithdrawalForm(data=form_data)
        self.assertIn('This field is required.', form.errors['currency'])
        self.assertFalse(form.is_valid())

    def test_form_missing_amount(self):
        form_data = {
            'currency': apps.get_model('concepts.Currency').objects.first().id,
        }
        form = CashFloatWithdrawalForm(data=form_data)
        self.assertIn('This field is required.', form.errors['amount'])
        self.assertFalse(form.is_valid())

    def test_form_negative_amount(self):
        form_data = {
            'currency': apps.get_model('concepts.Currency').objects.first().id,
            'amount': -200,
        }
        form = CashFloatWithdrawalForm(data=form_data)
        self.assertIn('Enter a positive amount.', form.errors['amount'])
        self.assertFalse(form.is_valid())

    def test_form_bad_amount(self):
        form_data = {
            'currency': apps.get_model('concepts.Currency').objects.first().id,
            'amount': 'f200',
        }
        form = CashFloatWithdrawalForm(data=form_data)
        self.assertIn('Enter a number.', form.errors['amount'])
        self.assertFalse(form.is_valid())

    def test_form_save(self):
        form_data = {
            'currency': apps.get_model('concepts.Currency').objects.first().id,
            'amount': 200,
        }
        form = CashFloatWithdrawalForm(data=form_data)
        transaction = apps.get_model('transactions.Transaction')(employee=self.admin)
        transaction.save()
        form.instance.transaction = transaction
        self.assertTrue(form.is_valid())
        instance = form.save()
        self.assertTrue(instance)


