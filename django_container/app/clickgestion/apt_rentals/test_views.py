from django.apps import apps
from clickgestion.core.test import CustomTestCase, CustomViewTestCase
from clickgestion.core import model_creation
from django.urls import reverse
from django.utils import timezone

app = 'apt_rentals'
concept = 'aptrental'


class ConceptNewViewTest(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_permission = '{}.add_{}'.format(app, concept)
        cls.url = '{}_new'.format(concept)
        cls.kwargs = {'transaction_code': model_creation.create_test_transaction(cls.admin, timezone.now())}
        cls.referer = '/'
        cls.get_template = 'concepts/concept_edit.html'


class ConceptDeleteViewTest(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_permission = '{}.add_{}'.format(app, concept)
        cls.url = '{}_delete'.format(concept)
        cls.kwargs = {'concept_code': getattr(cls, concept).code}
        cls.referer = '/'
        cls.get_template = 'core/delete.html'


class ConceptDetailViewTest(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_permission = '{}.add_{}'.format(app, concept)
        cls.url = '{}_detail'.format(concept)
        cls.kwargs = {'concept_code': getattr(cls, concept).code}
        cls.referer = '/'
        cls.get_template = 'concepts/concept_detail.html'


class ConceptEditlViewTest(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_permission = '{}.add_{}'.format(app, concept)
        cls.url = '{}_edit'.format(concept)
        cls.kwargs = {'concept_code': getattr(cls, concept).code}
        cls.referer = '/'
        cls.get_template = 'concepts/concept_edit.html'

