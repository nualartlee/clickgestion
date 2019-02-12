from clickgestion.core.test import CustomTestCase


class TestTransaction(CustomTestCase):

    def test_unicode(self):
        assert self.transaction.__unicode__()

    def test_client(self):
        assert self.transaction.client

    def test_description_short(self):
        assert self.transaction.description_short

    def test_total(self):
        assert self.transaction.total


