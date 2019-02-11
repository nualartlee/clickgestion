from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from clickgestion.transactions.models import Transaction
from clickgestion.apt_rentals.models import ApartmentRental, NightRateRange
from django.utils import timezone


class CustomTestCase(TestCase):  # pragma: no cover

    def setUp(self):
        test_name = self._testMethodName
        print('\n\n      ---- %s ----\n' % test_name)

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        # Create admin user
        user_name = 'admin'
        user_email = 'admin@here.com'
        user_pass = 'admin'
        cls.admin = User.objects.create_superuser(user_name, user_email, user_pass)
        # Create normal user
        user_name = 'test'
        user_email = 'test@here.com'
        user_pass = 'test'
        cls.normaluser = User.objects.create_user(user_name, user_email, user_pass)
        # Create transaction
        cls.transaction = Transaction.objects.create(
            user=cls.normaluser,
        )

        #
        # apt_rentals data
        #

        # Create a price range for the next year
        cls.night_rate_range = NightRateRange.objects.create(
            start_date=timezone.datetime.today(),
            end_date=timezone.datetime.today() + timezone.timedelta(days=730),
            monday=10,
            tuesday=20,
            wednesday=30,
            thursday=40,
            friday=50,
            saturday=60,
            sunday=70,
        )

        # Create an apartment rental
        cls.apartment_rental = ApartmentRental.objects.create(
            transaction=cls.transaction,
            checkin=timezone.datetime.today(),
            checkout=timezone.datetime.today() + timezone.timedelta(days=7),
        )

        print("\n\n============ %s ===============\n\n" % cls.__name__)

    def log_admin_in(self):
        self.client.force_login(self.admin)

    def log_normaluser_in(self):
        self.client.force_login(self.normaluser)


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
                self.assertTemplateUsed(response, 'littleserver_core/login.html')
            else:
                self.assertEqual(response.status_code, 403)
                self.assertTemplateUsed(response, 'littleserver_core/403.html')
        else:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.request['PATH_INFO'], reverse(self.url, kwargs=self.kwargs))
            self.assertTemplateUsed(response, self.get_template)

    def repeat_get(self):
        self.test_anonymous_get()
        self.test_normaluser_get()
        self.test_superuser_get()



