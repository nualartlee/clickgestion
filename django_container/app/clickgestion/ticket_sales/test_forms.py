from clickgestion.ticket_sales.forms import TicketSalesForm
from clickgestion.core.test import CustomTestCase
from clickgestion.core import model_creation
from django.utils import timezone


class TicketSalesFormTest(CustomTestCase):

    def test_form_ok(self):
        form_data = {
            'company': self.showcompany.id,
            'show': self.show.id,
            'adults': 2,
            'children': 0,
            'seniors': 0,
            'start_date': timezone.now(),
            'end_date': timezone.now() + timezone.timedelta(days=7),
        }
        form = TicketSalesForm(data=form_data)
        print(form_data)
        self.assertTrue(form.is_valid())

    def test_form_change_company(self):
        form_data = {
            'company': 2,
            'show': self.show.id,
            'adults': 2,
            'children': 0,
            'seniors': 0,
            'start_date': timezone.now(),
            'end_date': timezone.now() + timezone.timedelta(days=7),
        }
        form = TicketSalesForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_departure_before(self):
        form_data = {
            'company': self.showcompany.id,
            'show': self.show.id,
            'adults': 2,
            'children': 0,
            'seniors': 0,
            'start_date': '{}'.format(timezone.now().date()),
            'end_date': '{}'.format(timezone.now().date() - timezone.timedelta(days=1)),
        }
        form = TicketSalesForm(data=form_data)
        self.assertIn('End date is before start.', form.non_field_errors())
        self.assertFalse(form.is_valid())

    def test_form_no_start(self):
        form_data = {
            'company': self.showcompany.id,
            'show': self.show.id,
            'adults': 2,
            'children': 0,
            'seniors': 0,
            'end_date': timezone.now(),
        }
        form = TicketSalesForm(data=form_data)
        print(form.errors)
        self.assertIn('This field is required.', form.errors['start_date'])
        self.assertFalse(form.is_valid())

    def test_form_old_start_date(self):
        form_data = {
            'company': self.showcompany.id,
            'show': self.show.id,
            'adults': 2,
            'children': 0,
            'seniors': 0,
            'start_date': timezone.now() - timezone.timedelta(days=50),
            'end_date': timezone.now() - timezone.timedelta(days=45),
        }
        form = TicketSalesForm(data=form_data)
        self.assertIn('Ticket date is too far back.', form.errors['start_date'])
        self.assertFalse(form.is_valid())

    def test_form_save(self):
        transaction = model_creation.create_test_client_transaction(self.admin, timezone.now())
        adults = 2
        children = 1
        start_date = timezone.now()
        end_date = timezone.now() + timezone.timedelta(days=7)
        ticketsale = model_creation.create_test_ticketsale(
            transaction,
            timezone.now(),
            adults=adults,
            children=children,
            start_date=start_date,
            end_date=end_date,
        )
        form_data = {
            'company': self.showcompany.id,
            'show': self.show.id,
            'adults': adults,
            'children': children,
            'seniors': 0,
            'start_date': start_date,
            'end_date': end_date,
        }
        form = TicketSalesForm(data=form_data, instance=ticketsale)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())
