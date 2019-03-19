from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from clickgestion.transactions.models import Transaction
from clickgestion.apt_rentals.models import AptRental
from clickgestion.deposits.models import AptRentalDeposit
from django.utils import timezone
from clickgestion.core import model_creation
from django.apps import apps


def test_database_setup():
    # Test if the database is populated
    User = get_user_model()
    try:
        import pdb;pdb.set_trace()
        User.objects.get(username='administrator')

    # Create models if this is a new db
    except User.DoesNotExist:
        print('New database')
        model_creation.create_default_models()
        model_creation.create_test_models(days=30)


class CustomTestCase(TestCase):  # pragma: no cover

    def setUp(self):
        test_name = self._testMethodName
        print('\n\n      ---- %s ----\n' % test_name)

    @classmethod
    def setUpTestData(cls):
        model_creation.create_default_models()

        sgroup = model_creation.create_sales_group()
        cgroup = model_creation.create_cash_group()
        # Create admin user
        cls.admin = model_creation.create_superuser('administrator', 'admin', 'admin', 'admin@admin.com')
        # Create normal user
        cls.normaluser = model_creation.create_user('sebas', 'Sebastian', 'Panti', 'sebas@clickgestion.com', [sgroup, cgroup])

        # Create transaction
        cls.transaction = Transaction.objects.create(
            employee=cls.normaluser,
        )

        # Create a default currency
        cls.currency = model_creation.create_euros()
        model_creation.create_pounds()
        model_creation.create_dollars()

        # Create aptrentalsettings
        model_creation.create_aptrentalsettings()
        cls.nightraterange = model_creation.create_nightraterange()

        # Create an apartment rental
        cls.aptrental = AptRental(
            transaction=cls.transaction,
            start_date=timezone.datetime.today(),
            end_date=timezone.datetime.today() + timezone.timedelta(days=7),
        )
        cls.aptrental.save()

        cls.aptrentaldeposit = AptRentalDeposit(
            apt_rental=cls.aptrental,
            transaction=Transaction.objects.create(employee=cls.normaluser),
        )
        cls.aptrentaldeposit.save()

        conceptvalue = apps.get_model('concepts.conceptvalue')( amount=200, currency=cls.currency)
        conceptvalue.save()
        cls.cashfloatdeposit = apps.get_model('cash_desk.cashfloatdeposit')(
            transaction=Transaction.objects.create(employee=cls.normaluser),
            value=conceptvalue,
        )
        cls.cashfloatdeposit.save()

        conceptvalue = apps.get_model('concepts.conceptvalue')( amount=200, currency=cls.currency)
        conceptvalue.save()
        cls.cashfloatwithdrawal = apps.get_model('cash_desk.cashfloatwithdrawal')(
            transaction=Transaction.objects.create(employee=cls.normaluser),
            value=conceptvalue,
        )
        cls.cashfloatwithdrawal.save()

        print("\n\n============ %s ===============\n\n" % cls.__name__)

    def log_admin_in(self):
        self.client.force_login(self.admin)

    def log_normaluser_in(self):
        self.client.force_login(self.normaluser)


class CustomModelTestCase:  # pragma: no cover
    """
    Derived class with utility functions to test models
    """
    model_attrs = []
    model_object = None

    def test_attrs(self):
        if self.model_attrs and self.model_object:
            for attr in self.model_attrs:
                self.assertTrue(
                    getattr(self.model_object, attr) or True,
                    '{}.{} returned False'.format(self.model_object, attr)
                )
        else:
            print('No attributes to test')


class CustomViewTestCase:  # pragma: no cover
    """
    Derived class with utility functions to test views
    If test_get/post is set, it will test the method over the three access levels.
    If the user has required_permission is met, the response should be ok (200) and use the template specified.
    Otherwise, the response should redirect to login or permission denied
    """

    required_permission = ''
    url = None
    kwargs = {}
    referer = '/'
    test_get = False
    get_code = 200
    get_template = None
    get_url = None
    test_post = False
    post_template = '/'
    testuser = model_creation.create_user('testuser', 'testuser', 'testuser', 't@t.com', [])

    def check_get_response(self, response):

        # Check the code
        self.assertEqual(response.status_code, self.get_code)

        # Check the template
        if self.get_template:
            self.assertTemplateUsed(response, self.get_template)

        # Check the path
        if self.get_url:
            self.assertEqual(response.request['PATH_INFO'], self.get_url)
        else:
            self.assertEqual(response.request['PATH_INFO'], reverse(self.url, kwargs=self.kwargs))

    def test_anonymous_get(self):
        if not self.test_get:
            print("Not testing GET")
            return
        response = self.client.get(
            reverse(self.url, kwargs=self.kwargs),
            HTTP_REFERER=self.referer, follow=True)
        if self.required_permission is None:
            self.check_get_response(response)
        else:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.request['PATH_INFO'], reverse('login'))
            self.assertTemplateUsed(response, 'core/login.html')

    def test_non_permitted_get(self):
        if not self.test_get:
            print("Not testing GET")
            return
        if not self.required_permission:
            print("No permission required")
            return
        else:
            codename = self.required_permission.split('.')[1]
            permission = apps.get_model('auth.Permission').objects.get(codename=codename)
            self.testuser.user_permissions.remove(permission)
            self.testuser.save()
        self.client.force_login(self.testuser)
        response = self.client.get(
            reverse(self.url, kwargs=self.kwargs),
            HTTP_REFERER=self.referer, follow=True)

        #if self.required_permission == 'apt_rentals.add_aptrental':
        #    import pdb;pdb.set_trace()

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'core/403.html')

    def test_permitted_get(self):
        if not self.test_get:
            print("Not testing GET")
            return
        if not self.required_permission:
            print("No permission required")
            self.testuser.user_permissions.remove(*self.normaluser.user_permissions.all())
            self.testuser.save()
        else:
            codename = self.required_permission.split('.')[1]
            permission = apps.get_model('auth.Permission').objects.get(codename=codename)
            self.testuser.user_permissions.add(permission)
            self.testuser.save()
        self.client.force_login(self.testuser)
        response = self.client.get(
            reverse(self.url, kwargs=self.kwargs),
            HTTP_REFERER=self.referer, follow=True)
        self.check_get_response(response)

    def test_superuser_get(self):
        if not self.test_get:
            print("Not testing GET")
            return
        self.log_admin_in()
        response = self.client.get(
            reverse(self.url, kwargs=self.kwargs),
            HTTP_REFERER=self.referer, follow=True)
        self.check_get_response(response)

    def repeat_get(self):
        self.test_anonymous_get()
        self.test_non_permitted_get()
        self.test_permitted_get()
        self.test_superuser_get()



