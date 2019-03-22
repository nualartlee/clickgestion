from clickgestion.core.model_creation import create_test_transaction
from clickgestion.core.test import CustomTestCase, CustomViewTestCase
from importlib import import_module
from clickgestion.core import model_creation
from django.shortcuts import reverse
from django.conf import settings
from clickgestion.concepts import test_views
from django.utils import timezone

app = 'refunds'
concept = 'refund'


class RefundActionViewTest(test_views.ConceptActionsViewTest):

    app = app
    concept = concept


class RefundDeleteViewTest(test_views.ConceptDeleteViewTest):

    app = app
    concept = concept


class RefundDetailViewTest(test_views.ConceptDetailViewTest):

    app = app
    concept = concept


class RefundListViewTest(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_permission = 'refunds.add_refund'
        cls.url = 'refund_list'
        cls.kwargs = {}
        cls.referer = '/'
        cls.get_template = 'concepts/concept_list.html'


class RefundNewViewTest(test_views.ConceptNewViewTest):

    app = app
    concept = concept

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        if cls.app is not '':
            cls.test_get = True
            cls.required_permission = '{}.add_{}'.format(cls.app, cls.concept)
            cls.url = '{}_new'.format(cls.concept)
            cls.kwargs = {'transaction_code': create_test_transaction(cls.admin, timezone.now())}
            cls.referer = '/'
            cls.get_template = 'concepts/concept_list.html'
            cls.get_url = reverse('concept_list')

    def test_with_concept(self):
        # Create a deposit
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        transaction.close(self.admin)
        self.kwargs = {'concept_code': aptrental.code}
        self.get_url = 'pass'
        self.get_template = 'transactions/transaction_edit.html'
        self.repeat_get()

    def test_with_concept_and_transaction(self):
        # Create a deposit
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        transaction.close(self.admin)
        self.kwargs = {
            'concept_code': aptrental.code,
        }
        if self.client.session:  # pragma: no cover
            session = self.client.session
        else:  # pragma: no cover
            engine = import_module(settings.SESSION_ENGINE)
            session = engine.SessionStore()
        session['refund_transaction_code'] = create_test_transaction(self.admin, timezone.now()).code
        session.save()
        self.get_url = 'pass'
        self.get_template = 'transactions/transaction_edit.html'
        self.repeat_get()

    def test_with_nonreturnable_concept(self):
        # Create a deposit
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        self.kwargs = {'concept_code': aptrental.code}
        self.get_url = 'pass'
        self.get_template = 'core/message.html'
        self.repeat_get()


class RefundRowViewTest(test_views.ConceptRowViewTest):

    app = app
    concept = concept
