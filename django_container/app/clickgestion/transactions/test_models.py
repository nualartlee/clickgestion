from clickgestion.core.test import CustomTestCase


class TestTransaction(CustomTestCase):

    def test_unicode(self):
        assert self.transaction.__unicode__()



