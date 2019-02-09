from clickgestion.main.test import CustomTestCase


class TestTransaction(CustomTestCase):

    def test_unicode(self):
        assert self.transaction.__unicode__()



