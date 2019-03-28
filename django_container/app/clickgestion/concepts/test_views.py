from clickgestion.core.test import CustomTestCase, CustomViewTestCase
from clickgestion.core.model_creation import create_test_transaction
from django.utils import timezone
import urllib
from django.shortcuts import reverse
from clickgestion.concepts.views import get_transaction_from_kwargs, get_concept_and_form_from_kwargs
from django.urls.exceptions import Http404
from clickgestion.apt_rentals.forms import AptRentalForm


class ConceptActionsViewTest(CustomTestCase, CustomViewTestCase):  # pragma: no cover

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

    def test_filtered_ok(self):
        filter_data = {
            'accounting_group': 'Deposits',
        }
        params = urllib.parse.urlencode(filter_data)
        # Return
        url = reverse('concept_list')
        url += '?{}'.format(params)
        self.client.force_login(self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.get_template)


class ConceptNewViewTest(CustomTestCase, CustomViewTestCase):  # pragma: no cover

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


class ConceptDeleteViewTest(CustomTestCase, CustomViewTestCase):  # pragma: no cover

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


class ConceptDetailViewTest(CustomTestCase, CustomViewTestCase):  # pragma: no cover

    app = ''
    concept = ''

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        if cls.app is not '':
            cls.test_get = True
            cls.required_permission = '{}.add_{}'.format(cls.app, cls.concept)
            cls.url = '{}_detail'.format(cls.concept)
            concept = getattr(cls, cls.concept)
            concept.transaction.close(cls.admin)
            cls.kwargs = {'concept_code': concept.code}
            cls.referer = '/'
            cls.get_template = 'concepts/concept_detail.html'


class ConceptEditViewTest(CustomTestCase, CustomViewTestCase):  # pragma: no cover

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


class ConceptRowViewTest(CustomTestCase, CustomViewTestCase):  # pragma: no cover

    app = ''
    concept = ''

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        if cls.app is not '':
            cls.test_get = True
            cls.required_permission = ''
            cls.url = 'concept_row'
            cls.kwargs = {'concept_code': getattr(cls, cls.concept).code}
            cls.referer = '/'
            cls.get_template = 'concepts/concept_list.html'
            cls.get_url = reverse('concept_list')


class ConceptViewFunctionTest(CustomTestCase):

    def test_get_transaction_from_kwargs(self):
        kwargs = {'transaction_code': self.transaction.code}
        transaction = get_transaction_from_kwargs(**kwargs)
        self.assertEqual(transaction, self.transaction)
        kwargs = {'transaction_code': 'RR34343'}
        self.assertRaises(Http404, get_transaction_from_kwargs, **kwargs)

    def test_get_concept_and_form_from_kwargs(self):
        form = AptRentalForm
        # Returns new concept as it has a transaction code
        kwargs = {
            'concept_form': form,
            'transaction_code': self.transaction.code,
        }
        concept, form = get_concept_and_form_from_kwargs(**kwargs)
        self.assertEqual(concept.code, '')
        # Returns existing concept
        kwargs = {
            'concept_form': form,
            'concept_code': self.aptrental.code,
        }
        concept, form = get_concept_and_form_from_kwargs(**kwargs)
        self.assertEqual(concept, self.aptrental)

