from littleserverdjango.littleserver_core.test import LittleServerTestCase
from littleserverdjango.littleserver_core import wsgi


class TestWSGI(LittleServerTestCase):

    def test_wsgi(self):
        assert wsgi.application