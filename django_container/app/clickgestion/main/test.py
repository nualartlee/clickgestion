from django.urls import reverse
from django.test import TestCase


class LittleServerTestCase(TestCase):  # pragma: no cover

    def setUp(self):
        test_name = self._testMethodName
        print('\n\n      ---- %s ----\n' % test_name)

    @classmethod
    def setUpTestData(cls):
        cls.local_server = administration._create_local_server()
        cls.local_server.comm_configuration_status = cls.local_server.CommConfigStages.configured
        cls.local_server.save()
        cls.admin_pass = 'server'
        cls.admin = administration._create_admin()
        cls.admin.configuration_status = cls.admin.ConfigStages.configured
        cls.admin.save()

        # Server comm links
        # Create local dummy comm link
        cls.local_commlink = CommLink.objects.create(
            owner=cls.local_server,
            local=True,
            comm_module='littleserverdjango.littleserver_core.messaging_dummy')
        # Create a dummy encryption tool for the local comm link
        CryptoTool.objects.create(
            commlink=cls.local_commlink,
            local=True,
            crypto_module='littleserverdjango.littleserver_core.encryption_dummy')
        # Create remote dummy comm link
        cls.remote_commlink = CommLink.objects.create(
            owner=cls.local_server,
            local=False,
            comm_module='littleserverdjango.littleserver_core.messaging_dummy')
        # Create a dummy encryption tool for the remote tor link
        CryptoTool.objects.create(
            commlink=cls.remote_commlink,
            local=False,
            crypto_module='littleserverdjango.littleserver_core.encryption_dummy')

        # Admin comm links
        # Create local dummy comm link
        cls.admin_local_commlink = CommLink.objects.create(
            owner=cls.admin,
            local=True,
            comm_module='littleserverdjango.littleserver_core.messaging_dummy')
        # Create a dummy encryption tool for the local comm link
        CryptoTool.objects.create(
            commlink=cls.admin_local_commlink,
            local=True,
            crypto_module='littleserverdjango.littleserver_core.encryption_dummy')
        # Create remote dummy comm link
        cls.admin_remote_commlink = CommLink.objects.create(
            owner=cls.admin,
            local=False,
            comm_module='littleserverdjango.littleserver_core.messaging_dummy')
        # Create a dummy encryption tool for the remote tor link
        CryptoTool.objects.create(
            commlink=cls.admin_remote_commlink,
            local=False,
            crypto_module='littleserverdjango.littleserver_core.encryption_dummy')

        # Create local comm alarm
        cls.comm_alarm = event_handling.get_comm_alarm(cls.local_server)
        # Create a notification for the comm alarm
        cls.notification = Notification(
            event=cls.comm_alarm,
            commlink=cls.local_commlink,
        )
        cls.notification.save()

        # Create normal user
        cls.normaluser_name = 'testuser'
        cls.normaluser_email = 'testuser@here.com'
        cls.normaluser_pass = 'test'
        cls.normaluser = User(server=cls.local_server,
                          username=cls.normaluser_name,
                          email=cls.normaluser_email)
        cls.normaluser.set_password(cls.normaluser_pass)
        cls.normaluser.save()

        cls.admin.refresh_from_db()
        cls.local_server.refresh_from_db()

        print("\n\n============ %s ===============\n\n" % cls.__name__)

    def configure_all(self):
        self.configure_admin()
        self.configure_local_server()

    def configure_admin(self):
        admin = User.objects.get(id=0)
        admin.configuration_status = admin.ConfigStages.configured
        admin.save()
        self.admin.refresh_from_db()
        return admin

    def configure_local_server(self):
        local_server = LittleServer.objects.get(id=0)
        local_server.comm_configuration_status = LittleServer.CommConfigStages.configured
        local_server.save()
        self.local_server.refresh_from_db()
        return local_server

    @classmethod
    def create_new_server(cls):
        cls.new_server = LittleServer.objects.create(
            name='new_server',
            comm_configuration_status=LittleServer.CommConfigStages.invitation_created,
        )
        cls.new_local_commlink = CommLink.objects.create(
            local=True,
            owner=cls.new_server,
            comm_module='littleserver_core.messaging_dummy',
        )
        cls.new_remote_commlink = CommLink.objects.create(
            local=False,
            owner=cls.new_server,
            comm_module='littleserver_core.messaging_dummy',
        )
        cls.new_local_cryptotool = CryptoTool.objects.create(
            local=True,
            commlink=cls.new_local_commlink,
            crypto_module='littleserver_core.encryption_dummy',
        )
        cls.new_remote_cryptotool = CryptoTool.objects.create(
            local=False,
            commlink=cls.new_remote_commlink,
            crypto_module='littleserver_core.encryption_dummy',
        )
        return cls.new_server

    def log_admin_in(self):
        self.admin.set_password(self.admin_pass)
        self.admin.save()
        loggedin = self.client.login(username=self.admin.username, password=self.admin_pass)
        self.assertTrue(loggedin)
        return self.admin

    def log_normaluser_in(self):
        loggedin = self.client.login(username=self.normaluser_name,
                                     password=self.normaluser_pass)
        return loggedin


class LittleServerViewTests:  # pragma: no cover
    """
    Derived class with utility functions to test LittleServer views
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
        self.configure_admin()
        self.configure_local_server()
        response = self.client.get(
            reverse(self.url, kwargs=self.kwargs),
            HTTP_REFERER=self.referer, follow=True)
        self.check_response(True, response, 0)

    def test_normaluser_get(self):
        if not self.test_get:
            print("Not testing GET")
            return
        self.configure_all()
        self.log_normaluser_in()
        response = self.client.get(
            reverse(self.url, kwargs=self.kwargs),
            HTTP_REFERER=self.referer, follow=True)
        self.check_response(False, response, 1)

    def test_superuser_get(self):
        if not self.test_get:
            print("Not testing GET")
            return
        self.configure_all()
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



