from clickgestion.core.test import CustomTestCase
from clickgestion.apt_rentals.forms import AptRentalForm
from django.utils import timezone


class AptRentalFormTest(CustomTestCase):

    def test_form_ok(self):
        form_data = {
            'adults': 2,
            'children': 0,
            'start_date': timezone.now(),
            'end_date': timezone.now() + timezone.timedelta(days=7),
        }
        form = AptRentalForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_missing_prices(self):
        form_data = {
            'adults': 2,
            'children': 0,
            'start_date': timezone.now() + timezone.timedelta(days=1000),
            'end_date': timezone.now() + timezone.timedelta(days=1007),
        }
        form = AptRentalForm(data=form_data)
        self.assertIn('Missing prices in selected dates', form.non_field_errors())
        self.assertFalse(form.is_valid())
