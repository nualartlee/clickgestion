from clickgestion.core.test import CustomTestCase, CustomViewTestCase
from clickgestion.core.model_creation import create_test_transaction
from django.utils import timezone


class ConceptActionsViewTest(CustomTestCase, CustomViewTestCase):

    app = ''
    concept = ''

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        if cls.app is not '':
            cls.test_get = True
            cls.required_permission = ''
            cls.url = 'concept_actions'
            cls.kwargs = {'concept_code': getattr(cls, cls.concept).code}
            cls.referer = '/'
            cls.get_template = 'concepts/concept_actions.html'


class ConceptListViewTest(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_permission = ''
        cls.url = 'concept_list'
        cls.kwargs = {}
        cls.referer = '/'
        cls.get_template = 'concepts/concept_list.html'


class ConceptNewViewTest(CustomTestCase, CustomViewTestCase):

    app = ''
    concept = ''

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        if cls.app is not '':
            cls.test_get = True
            cls.required_permission = '{}.add_{}'.format(cls.app, cls.concept)
            cls.url = '{}_new'.format(cls.concept)
            cls.kwargs = {'transaction_code': create_test_transaction(cls.admin, timezone.now())}
            cls.referer = '/'
            cls.get_template = 'concepts/concept_edit.html'


class ConceptDeleteViewTest(CustomTestCase, CustomViewTestCase):

    app = ''
    concept = ''

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        if cls.app is not '':
            cls.test_get = True
            cls.required_permission = '{}.add_{}'.format(cls.app, cls.concept)
            cls.url = '{}_delete'.format(cls.concept)
            cls.kwargs = {'concept_code': getattr(cls, cls.concept).code}
            cls.referer = '/'
            cls.get_template = 'core/delete.html'


class ConceptDetailViewTest(CustomTestCase, CustomViewTestCase):

    app = ''
    concept = ''

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        if cls.app is not '':
            cls.test_get = True
            cls.required_permission = '{}.add_{}'.format(cls.app, cls.concept)
            cls.url = '{}_detail'.format(cls.concept)
            cls.kwargs = {'concept_code': getattr(cls, cls.concept).code}
            cls.referer = '/'
            cls.get_template = 'concepts/concept_detail.html'


class ConceptEditlViewTest(CustomTestCase, CustomViewTestCase):

    app = ''
    concept = ''

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        if cls.app is not '':
            cls.test_get = True
            cls.required_permission = '{}.add_{}'.format(cls.app, cls.concept)
            cls.url = '{}_edit'.format(cls.concept)
            cls.kwargs = {'concept_code': getattr(cls, cls.concept).code}
            cls.referer = '/'
            cls.get_template = 'concepts/concept_edit.html'
