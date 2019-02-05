from django.urls import reverse
from littleserverdjango.littleserver_core.test import LittleServerTestCase, LittleServerViewTests
from unittest import mock
from littleserverdjango.littleserver_users.models import User



class TestNotFoundView(LittleServerTestCase, LittleServerViewTests):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = False
        cls.required_access_level = 2
        cls.configure_local_server(cls)
        cls.configure_admin(cls)
        cls.url = 'serverdetail'
        cls.kwargs = {'server_id': 9999}
        cls.referer = '/'
        cls.get_template = 'littleserver_core/404.html'

    def test_custom_get(self):
        self.log_admin_in()
        response = self.client.get(reverse(self.url, kwargs=self.kwargs), follow=True)
        self.assertTemplateUsed(response, self.get_template)


class TestDefaultView(LittleServerTestCase, LittleServerViewTests):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = False
        cls.required_access_level = 0
        cls.configure_local_server(cls)
        cls.configure_admin(cls)
        cls.url = '/'
        cls.args = []
        cls.referer = '/'
        cls.get_template = 'littleserver_core/home.html'

    def test_get_requests_are_redirected(self):
        response = self.client.get('/', follow=False)
        self.assertTemplateUsed(response, 'littleserver_core/home.html')

    @mock.patch('littleserverdjango.littleserver_core.celery_app.tasks')
    def test_post_ok(self, mock_celery):
        mock_task = mock.Mock()
        mock_task.Delay.return_value = True
        mock_celery.get.return_value = mock_task
        post_data = {'data': 'rubbish'}
        response = self.client.post('/', post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'POST')


class TestHomeView(LittleServerTestCase, LittleServerViewTests):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_access_level = 0
        cls.configure_local_server(cls)
        cls.configure_admin(cls)
        cls.url = 'default'
        cls.args = []
        cls.referer = '/'
        cls.get_template = 'littleserver_core/home.html'

    def test_redirect_to_user_settings_for_new_admin(self):
        # Check it redirects to admin setup when not configured
        self.configure_all()
        self.admin.configuration_status = 'fresh'
        self.admin.save()
        response = self.client.get('/', follow=True)
        self.assertRedirects(response, '/users/%s/edit/' % self.admin.id)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'littleserver_users/useredit.html')

    def test_redirect_to_server_settings_for_new_server(self):
        # Check it redirects to server setup when not configured (and admin is)
        self.configure_all()
        self.log_admin_in()
        self.local_server.comm_configuration_status = self.local_server.CommConfigStages.invitation_created
        self.local_server.save()
        response = self.client.get('/', follow=True)
        self.assertRedirects(response, '/servers/%s/edit/' % self.local_server.id)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'littleserver_servers/serveredit.html')


class TestLoginView(LittleServerTestCase, LittleServerViewTests):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = False
        cls.required_access_level = 0
        cls.configure_local_server(cls)
        cls.configure_admin(cls)
        cls.url = 'login'
        cls.args = []
        cls.referer = '/'
        cls.get_template = 'littleserver_core/login.html'

    def test_get_ok(self):
        response = self.client.get(reverse('login'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], reverse('login'))
        self.assertTemplateUsed(response, 'littleserver_core/login.html')

    def test_post_no_data(self):
        response = self.client.post('/login/',
                                    {'username': '', 'password': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'littleserver_core/login.html')
        self.assertEqual(response.context['header'], 'Login Failed:')
        self.assertFormError(response, 'form', 'username', [u'This field is required.'])
        self.assertFormError(response, 'form', 'password', [u'This field is required.'])
    
    def test_post_wrong_data(self):
        response = self.client.post('/login/',
                                    {'username': 'nobody', 'password': 'nobodyspassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'littleserver_core/login.html')
        self.assertEqual(response.context['header'], 'Login Failed:')
    
    def test_post_right_data(self):
        # Will redirect to homeview by default when admin and server are configured
        response = self.client.post('/login/',
                                    {'username': self.normaluser_name,
                                     'password': self.normaluser_pass},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'littleserver_core/home.html')


class TestLogoutView(LittleServerTestCase, LittleServerViewTests):

    def test_get_logs_out(self):
        self.configure_admin()
        self.configure_local_server()
        self.log_admin_in()
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.get(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)


class TestForbiddenView(LittleServerTestCase, LittleServerViewTests):

    def test_get_custom(self):
        self.configure_all()
        self.log_normaluser_in()
        response = self.client.get(reverse('settings'), follow=True)
        self.assertEqual(response.status_code, 403)
