from django.apps import apps
from clickgestion.service_sales.forms import ServiceSalesForm
from clickgestion.core.test import CustomTestCase
from clickgestion.core import model_creation
from django.utils import timezone


class ServiceSalesFormTest(CustomTestCase):

    def run_service_tests(self, service):
        print('\nTesting Type: {}:{}\nService: {}:{}\n'.format(service.servicetype.id, service.servicetype.name, service.id, service.name))
        self.test_form_departure_before(service)
        if service.per_adult or service.per_child or service.per_senior:
            self.test_form_no_people(service)
        if service.per_night or service.date_required:
            self.test_form_no_start(service)
            self.test_form_old_start_date(service)
        self.test_form_ok(service)
        self.test_form_save(service)
        self.test_form_get_field_value(service)

    def test_all_services(self):
        services = apps.get_model('service_sales.Service').objects.filter(enabled=True)
        for service in services:
            self.run_service_tests(service)

    def test_form_no_people(self, service=None):
        if not service:
            service = self.service
        form_data = {
            'adults': 0,
            'children': 0,
            'end_date': timezone.now() + timezone.timedelta(days=7),
            'final_submit': True,
            'seniors': 0,
            'service': service.id,
            'start_date': timezone.now(),
            'type': service.servicetype.id,
        }
        form = ServiceSalesForm(data=form_data)
        message = '\nService: {}\nForm Data: {}\nErrors: {}\n'.format(service.name, form_data, form.errors)
        if service.per_adult or service.per_child or service.per_senior:
            self.assertIn('No people.', form.non_field_errors(), msg=message)
            self.assertFalse(form.is_valid(), msg=message)

    def test_form_ok(self, service=None):
        if not service:
            service = self.service
        form_data = {
            'adults': 1,
            'children': 1,
            'end_date': timezone.now() + timezone.timedelta(days=7),
            'final_submit': True,
            'seniors': 1,
            'service': service.id,
            'start_date': timezone.now(),
            'type': service.servicetype.id,
        }
        form = ServiceSalesForm(data=form_data)
        message = '\nService: {}\nForm Data: {}\nErrors: {}\n'.format(service.name, form_data, form.errors)
        self.assertTrue(
            form.is_valid(), msg=message)

    def test_form_departure_before(self, service=None):
        if not service:
            service = self.service
        if not service.per_night:
            return
        form_data = {
            'adults': 2,
            'children': 0,
            'end_date': '{}'.format(timezone.now().date() - timezone.timedelta(days=1)),
            'final_submit': True,
            'seniors': 0,
            'service': service.id,
            'start_date': '{}'.format(timezone.now().date()),
            'type': service.servicetype.id,
        }
        form = ServiceSalesForm(data=form_data)
        message = '\nService: {}\nForm Data: {}\nErrors: {}\n'.format(service.name, form_data, form.errors)
        self.assertIn('Ensure this value is greater than', form.errors['end_date'][0], msg=message)
        self.assertFalse(form.is_valid(), msg=message)

    def test_form_no_start(self, service=None):
        if not service:
            service = self.service
        if not service.date_required:
            return
        form_data = {
            'adults': 2,
            'children': 0,
            'end_date': timezone.now(),
            'final_submit': True,
            'seniors': 0,
            'service': service.id,
            'type': service.servicetype.id,
        }
        form = ServiceSalesForm(data=form_data)
        message = '\nService: {}\nForm Data: {}\nErrors: {}\n'.format(service.name, form_data, form.errors)
        self.assertIn('This field is required.', form.errors['start_date'], msg=message)
        self.assertFalse(form.is_valid(), msg=message)

    def test_form_old_start_date(self, service=None):
        if not service:
            service = self.service
        if not service.date_required:
            return
        form_data = {
            'adults': 2,
            'children': 0,
            'end_date': timezone.now() - timezone.timedelta(days=45),
            'final_submit': True,
            'seniors': 0,
            'service': service.id,
            'start_date': timezone.now() - timezone.timedelta(days=50),
            'type': service.servicetype.id,
        }
        form = ServiceSalesForm(data=form_data)
        message = '\nService: {}\nForm Data: {}\nErrors: {}\n'.format(service.name, form_data, form.errors)
        self.assertIn('Ticket date is too far back.', form.errors['start_date'], msg=message)
        self.assertFalse(form.is_valid(), msg=message)

    def test_form_save(self, service=None):
        if not service:
            service = self.service
        transaction = model_creation.create_test_client_transaction(self.admin, timezone.now())
        adults = 1
        children = 1
        seniors = 1
        start_date = timezone.now()
        end_date = timezone.now() + timezone.timedelta(days=7)
        servicesale = model_creation.create_test_servicesale(
            transaction,
            timezone.now(),
            adults=adults,
            children=children,
            end_date=end_date,
            seniors=seniors,
            service=service,
            start_date=start_date,
        )
        form_data = {
            'adults': adults,
            'children': children,
            'end_date': end_date,
            'final_submit': True,
            'seniors': seniors,
            'service': service.id,
            'start_date': start_date,
            'type': service.servicetype.id,
            'units': 1,
        }
        form = ServiceSalesForm(form_data, instance=servicesale)
        message = '\nService: {}\nForm Data: {}\nErrors: {}\n'.format(service.name, form_data, form.errors)
        self.assertTrue(form.is_valid(), msg=message)
        self.assertTrue(form.save(), msg=message)

    def test_form_save_closed(self, service=None):
        if not service:
            service = self.service
        transaction = model_creation.create_test_client_transaction(self.admin, timezone.now())
        adults = 1
        children = 1
        seniors = 1
        start_date = timezone.now()
        end_date = timezone.now() + timezone.timedelta(days=7)
        servicesale = model_creation.create_test_servicesale(
            transaction,
            timezone.now(),
            adults=adults,
            children=children,
            end_date=end_date,
            seniors=seniors,
            service=service,
            start_date=start_date,
        )
        transaction.close(self.admin)
        form_data = {
            'adults': adults,
            'children': children,
            'end_date': end_date,
            'final_submit': True,
            'seniors': seniors,
            'service': service.id,
            'start_date': start_date,
            'type': service.servicetype.id,
            'units': 1,
        }
        form = ServiceSalesForm(form_data, instance=servicesale)
        message = '\nService: {}\nForm Data: {}\nErrors: {}\n'.format(service.name, form_data, form.errors)
        self.assertTrue(form.is_valid(), msg=message)
        self.assertTrue(form.save(), msg=message)

    def test_form_get_field_value(self, service=None):
        if not service:
            service = self.service
        form_real_data = {
            'adults': 3,
            'children': 3,
            'end_date': (timezone.now() + timezone.timedelta(days=7)).date(),
            'final_submit': True,
            'seniors': 3,
            'service': service,
            'start_date': timezone.now().date(),
            'type': service.servicetype,
            'units': 3,
        }
        form_data = {
            'adults': 3,
            'children': 3,
            'end_date': timezone.now() + timezone.timedelta(days=7),
            'final_submit': True,
            'seniors': 3,
            'service': service.id,
            'start_date': timezone.now(),
            'type': service.servicetype.id,
            'units': 3,
        }
        form = ServiceSalesForm(data=form_data)
        message = '\nService: {}\nForm Data: {}\nErrors: {}\n'.format(service.name, form_data, form.errors)
        for field in form.fields:
            if not form.fields[field].disabled:
                if form_real_data.get(field, False):
                    self.assertEqual(form.get_field_value(field), form_real_data[field], msg=message)
            else:
                self.assertEqual(form.get_field_value(field), form.initial[field], msg=message)
        # Test validation error
        field = 'service'
        form_data[field] = 'sadfasd'
        form = ServiceSalesForm(data=form_data)
        self.assertEqual(form.get_field_value(field), form.initial[field], msg=message)

    def test_form_varied_services(self):
        service = model_creation.create_service(
            model_creation.create_servicetype('Test Inc.'),
            'Test Service 1',
            date_required=True,
            per_adult=True,
            per_child=True,
            per_night=True,
            per_senior=True,
            per_unit=False,
            variable_price=True,
        )
        self.run_service_tests(service)
        service = model_creation.create_service(
            model_creation.create_servicetype('Test Inc.'),
            'Test Service 2',
            date_required=True,
            per_adult=False,
            per_child=False,
            per_night=True,
            per_senior=False,
            per_unit=False,
            variable_price=True,
        )
        self.run_service_tests(service)



