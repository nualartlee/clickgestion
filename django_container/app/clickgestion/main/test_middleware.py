from littleserverdjango.littleserver_core.test import LittleServerTestCase
from littleserverdjango.littleserver_core.middleware import LittleServerMiddleware
from littleserverdjango.littleserver_core.views import homeview
from django.http import HttpRequest
from django.shortcuts import reverse


class TestLittleServerMiddleware(LittleServerTestCase):

    def test_redirect_admin(self):
        self.configure_all()
        self.admin.configuration_status = 'fresh'
        self.admin.save()
        littleservermiddleware = LittleServerMiddleware(homeview)
        request = HttpRequest()
        request.session = self.client.session
        request.path = reverse('default')
        result = littleservermiddleware(request)
        assert result.url == reverse('useredit', kwargs={'user_id': self.admin.id})
        assert result.status_code == 302

    def test_no_redirect_admin(self):
        self.configure_all()
        littleservermiddleware = LittleServerMiddleware(homeview)
        request = HttpRequest()
        request.session = self.client.session
        request.path = reverse('default')
        result = littleservermiddleware(request)
        assert result.status_code == 200

    def test_redirect_server(self):
        self.configure_all()
        self.local_server.comm_configuration_status = 'fresh'
        self.local_server.save()
        littleservermiddleware = LittleServerMiddleware(homeview)
        request = HttpRequest()
        request.session = self.client.session
        request.path = reverse('default')
        result = littleservermiddleware(request)
        assert result.url == reverse('serveredit', kwargs={'server_id': self.local_server.id})
        assert result.status_code == 302

    def test_no_redirect_server(self):
        self.configure_all()
        littleservermiddleware = LittleServerMiddleware(homeview)
        request = HttpRequest()
        request.session = self.client.session
        request.path = reverse('default')
        result = littleservermiddleware(request)
        assert result.status_code == 200


