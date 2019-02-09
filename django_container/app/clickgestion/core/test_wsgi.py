from clickgestion.core.test import CustomTestCase
from clickgestion import wsgi


class TestWSGI(CustomTestCase):

    def test_wsgi(self):
        assert wsgi.application