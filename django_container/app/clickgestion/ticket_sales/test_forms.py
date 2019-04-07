from clickgestion.ticket_sales.forms import TicketSalesForm
from clickgestion.core.test import CustomTestCase
from clickgestion.core import model_creation
from django.utils import timezone


class TicketSalesFormTest(CustomTestCase):

    def test_form_ok(self):
        form_data = {
            'adults': 2,
            'children': 0,
            'start_date': timezone.now(),
            'end_date': timezone.now() + timezone.timedelta(days=7),
        }
        form = TicketSalesForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_many_adults(self):
        form_data = {
            'adults': 5,
            'children': 0,
            'start_date': timezone.now(),
            'end_date': timezone.now() + timezone.timedelta(days=7),
        }
        form = TicketSalesForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('One to four adults only.', form.errors['adults'])

    def test_form_many_children(self):
        form_data = {
            'adults': 2,
            'children': 5,
            'start_date': timezone.now(),
            'end_date': timezone.now() + timezone.timedelta(days=7),
        }
        form = TicketSalesForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Up to four children only.', form.errors['children'])

    def test_form_many_people(self):
        form_data = {
            'adults': 3,
            'children': 3,
            'start_date': timezone.now(),
            'end_date': timezone.now() + timezone.timedelta(days=7),
        }
        form = TicketSalesForm(data=form_data)
        self.assertIn('Five people maximum.', form.non_field_errors())
        self.assertFalse(form.is_valid())

    def test_form_missing_prices(self):
        form_data = {
            'adults': 2,
            'children': 0,
            'start_date': timezone.now() + timezone.timedelta(days=1000),
            'end_date': timezone.now() + timezone.timedelta(days=1007),
        }
        form = TicketSalesForm(data=form_data)
        self.assertIn('Missing prices in selected dates.', form.non_field_errors())
        self.assertFalse(form.is_valid())

    def test_form_departure_before(self):
        form_data = {
            'adults': 2,
            'children': 0,
            'start_date': '{}'.format(timezone.now().date()),
            'end_date': '{}'.format(timezone.now().date() - timezone.timedelta(days=1)),
        }
        form = TicketSalesForm(data=form_data)
        self.assertIn('Departure date is before arrival.', form.non_field_errors())
        self.assertFalse(form.is_valid())

    def test_form_departure_same(self):
        form_data = {
            'adults': 2,
            'children': 0,
            'start_date': '{}'.format(timezone.now().date()),
            'end_date': '{}'.format(timezone.now().date()),
        }
        form = TicketSalesForm(data=form_data)
        self.assertIn('Departure date is the same as arrival.', form.non_field_errors())
        self.assertFalse(form.is_valid())

    def test_form_no_start(self):
        form_data = {
            'adults': 2,
            'children': 0,
            'end_date': timezone.now(),
        }
        form = TicketSalesForm(data=form_data)
        print(form.errors)
        self.assertIn('This field is required.', form.errors['start_date'])
        self.assertFalse(form.is_valid())

    def test_form_old_start_date(self):
        form_data = {
            'adults': 2,
            'children': 0,
            'start_date': timezone.now() - timezone.timedelta(days=50),
            'end_date': timezone.now() - timezone.timedelta(days=45),
        }
        form = TicketSalesForm(data=form_data)
        self.assertIn('Arrival date is too far back.', form.errors['start_date'])
        self.assertFalse(form.is_valid())

    def test_save(self):
        transaction = model_creation.create_test_client_transaction(self.admin, timezone.now())
        adults = 2
        children = 1
        start_date = timezone.now()
        end_date = timezone.now() + timezone.timedelta(days=7)
        ticket_sale = model_creation.create_test_ticketsale(
            transaction,
            timezone.now(),
            adults=adults,
            children=children,
            start_date=start_date,
            end_date=end_date,
        )
        form_data = {
            'adults': adults,
            'children': children,
            'start_date': start_date,
            'end_date': end_date,
            'add_deposit': False,
        }
        form = TicketSalesForm(data=form_data, instance=ticketsale)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_save_with_deposit(self):
        transaction = model_creation.create_test_client_transaction(self.admin, timezone.now())
        adults = 2
        children = 1
        start_date = timezone.now()
        end_date = timezone.now() + timezone.timedelta(days=7)
        ticket_sale = model_creation.create_test_ticketsale(
            transaction,
            timezone.now(),
            adults=adults,
            children=children,
            start_date=start_date,
            end_date=end_date,
        )
        form_data = {
            'adults': adults,
            'children': children,
            'start_date': start_date,
            'end_date': end_date,
            'add_deposit': True,
        }
        form = TicketSalesForm(data=form_data, instance=ticketsale)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())
