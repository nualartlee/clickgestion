from django.urls import reverse
from clickgestion.core.test import CustomTestCase, CustomViewTestCase
import urllib


class TestConceptListView(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_access_level = 1
        cls.url = 'concept_list'
        cls.kwargs = {}
        cls.referer = '/'
        cls.get_template = 'concepts/concept_list.html'


class TestDepositListView(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_access_level = 1
        cls.url = 'deposit_list'
        cls.kwargs = {}
        cls.referer = '/'
        cls.get_template = 'concepts/concept_list.html'

    def test_returned_filter(self):
        self.log_admin_in()
        filter_data = {
            'returned': 3,
        }
        params = urllib.parse.urlencode(filter_data)
        url = reverse(self.url) + '?{}'.format(params)
        # Return
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'concepts/concept_list.html')
        self.assertEqual(response.status_code, 200)
