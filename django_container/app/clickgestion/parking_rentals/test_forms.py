from clickgestion.parking_rentals.forms import ParkingRentalForm
from clickgestion.core.test import CustomTestCase
from clickgestion.core import model_creation
from django.utils import timezone


class ParkingRentalFormTest(CustomTestCase):

    def test_form_ok(self):
        form_data = {
            'start_date': timezone.now(),
            'end_date': timezone.now() + timezone.timedelta(days=7),
        }
        form = ParkingRentalForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_departure_before(self):
        form_data = {
            'start_date': '{}'.format(timezone.now().date()),
            'end_date': '{}'.format(timezone.now().date() - timezone.timedelta(days=1)),
        }
        form = ParkingRentalForm(data=form_data)
        self.assertIn('Departure date is before arrival.', form.non_field_errors())
        self.assertFalse(form.is_valid())

    def test_form_departure_same(self):
        form_data = {
            'start_date': '{}'.format(timezone.now().date()),
            'end_date': '{}'.format(timezone.now().date()),
        }
        form = ParkingRentalForm(data=form_data)
        self.assertIn('Departure date is the same as arrival.', form.non_field_errors())
        self.assertFalse(form.is_valid())

    def test_form_no_start(self):
        form_data = {
            'end_date': timezone.now(),
        }
        form = ParkingRentalForm(data=form_data)
        print(form.errors)
        self.assertIn('This field is required.', form.errors['start_date'])
        self.assertFalse(form.is_valid())

    def test_form_old_start_date(self):
        form_data = {
            'start_date': timezone.now() - timezone.timedelta(days=50),
            'end_date': timezone.now() - timezone.timedelta(days=45),
        }
        form = ParkingRentalForm(data=form_data)
        self.assertIn('Arrival date is too far back.', form.errors['start_date'])
        self.assertFalse(form.is_valid())

    def test_save(self):
        transaction = model_creation.create_test_client_transaction(self.admin, timezone.now())
        start_date = timezone.now()
        end_date = timezone.now() + timezone.timedelta(days=7)
        ParkingRental = model_creation.create_test_parkingrental(
            transaction,
            timezone.now(),
            start_date=start_date,
            end_date=end_date,
        )
        form_data = {
            'start_date': start_date,
            'end_date': end_date,
            'add_deposit': False,
        }
        form = ParkingRentalForm(data=form_data, instance=ParkingRental)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_save_with_deposit(self):
        transaction = model_creation.create_test_client_transaction(self.admin, timezone.now())
        start_date = timezone.now()
        end_date = timezone.now() + timezone.timedelta(days=7)
        ParkingRental = model_creation.create_test_parkingrental(
            transaction,
            timezone.now(),
            start_date=start_date,
            end_date=end_date,
        )
        form_data = {
            'start_date': start_date,
            'end_date': end_date,
            'add_deposit': True,
        }
        form = ParkingRentalForm(data=form_data, instance=ParkingRental)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())
