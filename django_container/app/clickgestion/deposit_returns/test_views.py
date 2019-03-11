from clickgestion.core.test import CustomTestCase, CustomViewTestCase


class TestTodayView(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_access_level = 1
        cls.url = 'concept_list'
        cls.kwargs = {}
        cls.referer = '/'
        cls.get_template = 'transactions/concept_list.html'

