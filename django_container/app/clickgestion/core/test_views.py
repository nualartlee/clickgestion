from django.urls import reverse
from clickgestion.core.test import CustomTestCase, CustomViewTestCase
from clickgestion.core.views import message


class TestNotFoundView(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = False
        cls.required_access_level = 2
        cls.url = 'transaction_row'
        cls.kwargs = {'transaction_code': 'T0223456456'}
        cls.referer = '/'
        cls.get_template = 'core/404.html'

    def test_custom_get(self):
        self.log_admin_in()
        response = self.client.get(reverse(self.url, kwargs=self.kwargs), follow=True)
        self.assertTemplateUsed(response, self.get_template)


class TestIndexView(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = False
        cls.required_access_level = 0
        cls.url = '/'
        cls.kwargs = {}
        cls.referer = '/'
        cls.get_template = 'core/index.html'


class TestLoginView(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = False
        cls.required_access_level = 0
        cls.url = 'login'
        cls.kwargs = {}
        cls.referer = '/'
        cls.get_template = 'core/login.html'

    def test_get_ok(self):
        response = self.client.get(reverse('login'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], reverse('login'))
        self.assertTemplateUsed(response, 'core/login.html')

    def test_post_no_data(self):
        response = self.client.post('/login/',
                                    {'username': '', 'password': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')
        self.assertFormError(response, 'form', 'username', [u'This field is required.'])
        self.assertFormError(response, 'form', 'password', [u'This field is required.'])
    
    def test_post_wrong_data(self):
        response = self.client.post('/login/',
                                    {'username': 'nobody', 'password': 'nobodyspassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')

    def test_post_right_data(self):
        # Will redirect to homeview by default when admin and server are configured
        response = self.client.post('/login/',
                                    {'username': 'administrator',
                                     'password': 'administrator'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')


class TestLogoutView(CustomTestCase, CustomViewTestCase):

    def test_get_logs_out(self):
        self.log_admin_in()
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.get(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)


class TestMessageView(CustomTestCase, CustomViewTestCase):

    def test_message_view(self):
        request = self.client.request()
        response = message(request, {})
        self.assertEqual(response.status_code, 200)


class TestForbiddenView(CustomTestCase, CustomViewTestCase):

    def test_get_custom(self):
        self.log_normaluser_in()
        response = self.client.get(reverse('cash_desk_close'), follow=True)
        self.assertEqual(response.status_code, 403)

