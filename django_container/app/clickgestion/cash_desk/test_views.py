from django.urls import reverse
from clickgestion.core.test import CustomTestCase, CustomViewTestCase

class TestCashBalanceView(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_access_level = 1
        cls.url = 'cash_balance'
        cls.kwargs = {}
        cls.referer = '/'
        cls.get_template = 'transactions/cash_balance.html'


class TestCashCloseView(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_access_level = 1
        cls.url = 'cash_close'
        cls.kwargs = {}
        cls.referer = '/'
        cls.get_template = 'transactions/cash_close.html'

    def test_post_ok(self):
        self.log_admin_in()
        response = self.client.post(
            reverse(self.url, kwargs=self.kwargs),
            follow=True,
        )
        self.assertTemplateUsed(response, 'core/message.html')
        self.assertEqual(response.status_code, 200)
