from django.urls import reverse
from clickgestion.core.test import CustomTestCase, CustomViewTestCase
import urllib
from django.apps import apps


class ConceptActionsViewTest(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_permission = ''
        cls.url = 'concept_actions'
        cls.kwargs = {'concept_code': apps.get_model('concepts.BaseConcept').objects.first().code}
        cls.referer = '/'
        cls.get_template = 'concepts/concept_actions.html'


class ConceptDeleteViewTest(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_permission = 'concepts.add_concept'
        cls.url = 'concept_delete'
        cls.kwargs = {'concept_code': apps.get_model('concepts.BaseConcept').objects.first().code}
        cls.referer = '/'
        cls.get_template = 'core/delete.html'


class ConceptDetailViewTest(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_permission = ''
        cls.url = 'concept_detail'
        cls.kwargs = {'concept_code': apps.get_model('concepts.BaseConcept').objects.first().code}
        cls.referer = '/'
        cls.get_template = 'concepts/concept_detail.html'


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
