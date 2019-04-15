from django.apps import apps
from clickgestion.ticket_sales.forms import TicketSalesForm
from clickgestion.core.test import CustomTestCase
from clickgestion.core import model_creation
from django.utils import timezone


class TicketSalesFormTest(CustomTestCase):

    def run_show_tests(self, show):
        print('\nTesting Company: {}:{}\nShow: {}:{}\n'.format(show.company.id, show.company.name, show.id, show.name))
        self.test_form_departure_before(show)
        if show.per_adult or show.per_child or show.per_senior:
            self.test_form_no_people(show)
        if show.per_night or show.date_required:
            self.test_form_no_start(show)
            self.test_form_old_start_date(show)
        self.test_form_ok(show)
        self.test_form_save(show)
        self.test_form_get_field_value(show)

    def test_all_shows(self):
        shows = apps.get_model('ticket_sales.Show').objects.filter(enabled=True)
        for show in shows:
            self.run_show_tests(show)

    def test_form_no_people(self, show=None):
        if not show:
            show = self.show
        form_data = {
            'adults': 0,
            'children': 0,
            'company': show.company.id,
            'end_date': timezone.now() + timezone.timedelta(days=7),
            'final_submit': True,
            'seniors': 0,
            'show': show.id,
            'start_date': timezone.now(),
        }
        form = TicketSalesForm(data=form_data)
        message = '\nShow: {}\nForm Data: {}\nErrors: {}\n'.format(show.name, form_data, form.errors)
        if show.per_adult or show.per_child or show.per_senior:
            self.assertIn('No people.', form.non_field_errors(), msg=message)
            self.assertFalse(form.is_valid(), msg=message)

    def test_form_ok(self, show=None):
        if not show:
            show = self.show
        form_data = {
            'adults': 1,
            'children': 1,
            'company': show.company.id,
            'end_date': timezone.now() + timezone.timedelta(days=7),
            'final_submit': True,
            'seniors': 1,
            'show': show.id,
            'start_date': timezone.now(),
        }
        form = TicketSalesForm(data=form_data)
        message = '\nShow: {}\nForm Data: {}\nErrors: {}\n'.format(show.name, form_data, form.errors)
        self.assertTrue(
            form.is_valid(), msg=message)

    def test_form_departure_before(self, show=None):
        if not show:
            show = self.show
        if not show.per_night:
            return
        form_data = {
            'adults': 2,
            'children': 0,
            'company': show.company.id,
            'end_date': '{}'.format(timezone.now().date() - timezone.timedelta(days=1)),
            'final_submit': True,
            'seniors': 0,
            'show': show.id,
            'start_date': '{}'.format(timezone.now().date()),
        }
        form = TicketSalesForm(data=form_data)
        message = '\nShow: {}\nForm Data: {}\nErrors: {}\n'.format(show.name, form_data, form.errors)
        self.assertIn('Ensure this value is greater than', form.errors['end_date'][0], msg=message)
        self.assertFalse(form.is_valid(), msg=message)

    def test_form_no_start(self, show=None):
        if not show:
            show = self.show
        if not show.date_required:
            return
        form_data = {
            'adults': 2,
            'children': 0,
            'company': show.company.id,
            'end_date': timezone.now(),
            'final_submit': True,
            'show': show.id,
            'seniors': 0,
        }
        form = TicketSalesForm(data=form_data)
        message = '\nShow: {}\nForm Data: {}\nErrors: {}\n'.format(show.name, form_data, form.errors)
        self.assertIn('This field is required.', form.errors['start_date'], msg=message)
        self.assertFalse(form.is_valid(), msg=message)

    def test_form_old_start_date(self, show=None):
        if not show:
            show = self.show
        if not show.date_required:
            return
        form_data = {
            'adults': 2,
            'children': 0,
            'company': show.company.id,
            'end_date': timezone.now() - timezone.timedelta(days=45),
            'final_submit': True,
            'seniors': 0,
            'show': show.id,
            'start_date': timezone.now() - timezone.timedelta(days=50),
        }
        form = TicketSalesForm(data=form_data)
        message = '\nShow: {}\nForm Data: {}\nErrors: {}\n'.format(show.name, form_data, form.errors)
        self.assertIn('Ticket date is too far back.', form.errors['start_date'], msg=message)
        self.assertFalse(form.is_valid(), msg=message)

    def test_form_save(self, show=None):
        if not show:
            show = self.show
        transaction = model_creation.create_test_client_transaction(self.admin, timezone.now())
        adults = 1
        children = 1
        seniors = 1
        start_date = timezone.now()
        end_date = timezone.now() + timezone.timedelta(days=7)
        ticketsale = model_creation.create_test_ticketsale(
            transaction,
            timezone.now(),
            adults=adults,
            children=children,
            end_date=end_date,
            seniors=seniors,
            show=show,
            start_date=start_date,
        )
        form_data = {
            'adults': adults,
            'children': children,
            'company': show.company.id,
            'end_date': end_date,
            'final_submit': True,
            'seniors': seniors,
            'show': show.id,
            'start_date': start_date,
            'units': 1,
        }
        form = TicketSalesForm(form_data, instance=ticketsale)
        message = '\nShow: {}\nForm Data: {}\nErrors: {}\n'.format(show.name, form_data, form.errors)
        self.assertTrue(form.is_valid(), msg=message)
        self.assertTrue(form.save(), msg=message)

    def test_form_save_closed(self, show=None):
        if not show:
            show = self.show
        transaction = model_creation.create_test_client_transaction(self.admin, timezone.now())
        adults = 1
        children = 1
        seniors = 1
        start_date = timezone.now()
        end_date = timezone.now() + timezone.timedelta(days=7)
        ticketsale = model_creation.create_test_ticketsale(
            transaction,
            timezone.now(),
            adults=adults,
            children=children,
            end_date=end_date,
            seniors=seniors,
            show=show,
            start_date=start_date,
        )
        transaction.close(self.admin)
        form_data = {
            'adults': adults,
            'children': children,
            'company': show.company.id,
            'end_date': end_date,
            'final_submit': True,
            'seniors': seniors,
            'show': show.id,
            'start_date': start_date,
            'units': 1,
        }
        form = TicketSalesForm(form_data, instance=ticketsale)
        message = '\nShow: {}\nForm Data: {}\nErrors: {}\n'.format(show.name, form_data, form.errors)
        self.assertTrue(form.is_valid(), msg=message)
        self.assertTrue(form.save(), msg=message)

    def test_form_get_field_value(self, show=None):
        if not show:
            show = self.show
        form_real_data = {
            'adults': 3,
            'children': 3,
            'company': show.company,
            'end_date': (timezone.now() + timezone.timedelta(days=7)).date(),
            'final_submit': True,
            'seniors': 3,
            'show': show,
            'start_date': timezone.now().date(),
            'units': 3,
        }
        form_data = {
            'adults': 3,
            'children': 3,
            'company': show.company.id,
            'end_date': timezone.now() + timezone.timedelta(days=7),
            'final_submit': True,
            'seniors': 3,
            'show': show.id,
            'start_date': timezone.now(),
            'units': 3,
        }
        form = TicketSalesForm(data=form_data)
        message = '\nShow: {}\nForm Data: {}\nErrors: {}\n'.format(show.name, form_data, form.errors)
        for field in form.fields:
            if not form.fields[field].disabled:
                if form_real_data.get(field, False):
                    self.assertEqual(form.get_field_value(field), form_real_data[field], msg=message)
            else:
                self.assertEqual(form.get_field_value(field), form.initial[field], msg=message)
        # Test validation error
        field = 'show'
        form_data[field] = 'sadfasd'
        form = TicketSalesForm(data=form_data)
        self.assertEqual(form.get_field_value(field), form.initial[field], msg=message)

    def test_form_varied_shows(self):
        show = model_creation.create_show(
            model_creation.create_showcompany('Test Inc.'),
            'Test Show 1',
            date_required=True,
            per_adult=True,
            per_child=True,
            per_night=True,
            per_senior=True,
            per_unit=True,
            variable_price=True,
        )
        self.run_show_tests(show)
        show = model_creation.create_show(
            model_creation.create_showcompany('Test Inc.'),
            'Test Show 2',
            date_required=True,
            per_adult=False,
            per_child=False,
            per_night=True,
            per_senior=False,
            per_unit=False,
            variable_price=True,
        )
        self.run_show_tests(show)



