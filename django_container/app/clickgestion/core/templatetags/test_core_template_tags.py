from clickgestion.core.test import CustomTestCase
import clickgestion.core.templatetags.core_template_tags as tags
from django.test.client import RequestFactory


class TestCoreTemplateTags(CustomTestCase):

    def test_update_query_params(self):
        initial_params = 'closed=False'
        request = RequestFactory().get('/transactions/?{}'.format(initial_params))
        updated_params = tags.update_query_params(request, client_first_name='Fred')
        self.assertIn(initial_params, updated_params)




