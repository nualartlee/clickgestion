from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from clickgestion.transactions.models import Transaction
from clickgestion.apt_rentals.models import AptRental
from clickgestion.deposits.models import AptRentalDeposit
from django.utils import timezone
from clickgestion.core import model_creation


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
        cls.night_rate_range = model_creation.create_nightraterange()

        # Create an apartment rental
        cls.apartment_rental = AptRental(
            transaction=cls.transaction,
            start_date=timezone.datetime.today(),
            end_date=timezone.datetime.today() + timezone.timedelta(days=7),
        )
        cls.apartment_rental.save()

        cls.apartment_rental_deposit = AptRentalDeposit(
            apt_rental=cls.apartment_rental,
            transaction=Transaction.objects.create(employee=cls.normaluser),
        )
        cls.apartment_rental_deposit.save()

        print("\n\n============ %s ===============\n\n" % cls.__name__)

    def log_admin_in(self):
        self.client.force_login(self.admin)

    def log_normaluser_in(self):
        self.client.force_login(self.normaluser)


class CustomModelTestCase: # pragma: no cover
    """
    Derived class with utility functions to test models
    """
    model_attrs = []
    model_object = None

    def test_attrs(self):
        if self.model_attrs and self.model_object:
            for attr in self.model_attrs:
                assert getattr(self.model_object, attr)
        else:
            print('No attributes to test')


class CustomViewTestCase:  # pragma: no cover
    """
    Derived class with utility functions to test views
    If test_get/post is set, it will test the method over the three access levels.
    If access level is met, the response should be ok (200) and use the template specified.
    Otherwise, the response should redirect to login
    """
    class AccessLevels:
        anyone = 0
        normal_user = 1
        administrator = 2

    required_access_level = AccessLevels.anyone
    url = None
    kwargs = {}
    referer = '/'
    test_get = False
    get_template = '/'
    test_post = False
    post_template = '/'

    def test_anonymous_get(self):
        if not self.test_get:
            print("Not testing GET")
            return
        response = self.client.get(
            reverse(self.url, kwargs=self.kwargs),
            HTTP_REFERER=self.referer, follow=True)
        self.check_response(True, response, 0)

    def test_normaluser_get(self):
        if not self.test_get:
            print("Not testing GET")
            return
        self.log_normaluser_in()
        response = self.client.get(
            reverse(self.url, kwargs=self.kwargs),
            HTTP_REFERER=self.referer, follow=True)
        self.check_response(False, response, 1)

    def test_superuser_get(self):
        if not self.test_get:
            print("Not testing GET")
            return
        self.log_admin_in()
        response = self.client.get(
            reverse(self.url, kwargs=self.kwargs),
            HTTP_REFERER=self.referer, follow=True)
        self.check_response(False, response, 2)

    def check_response(self, anonymous, response, access_level):
        if self.required_access_level > access_level:
            if anonymous:
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.request['PATH_INFO'], reverse('login'))
                self.assertTemplateUsed(response, 'core/login.html')
            else:
                self.assertEqual(response.status_code, 403)
                self.assertTemplateUsed(response, 'core/403.html')
        else:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.request['PATH_INFO'], reverse(self.url, kwargs=self.kwargs))
            self.assertTemplateUsed(response, self.get_template)

    def repeat_get(self):
        self.test_anonymous_get()
        self.test_normaluser_get()
        self.test_superuser_get()



