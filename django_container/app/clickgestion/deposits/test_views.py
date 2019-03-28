from clickgestion.core.model_creation import create_test_transaction
from clickgestion.core.test import CustomTestCase, CustomViewTestCase
from importlib import import_module
from clickgestion.core import model_creation
from django.shortcuts import reverse
from django.conf import settings
from clickgestion.concepts import test_views
from django.utils import timezone

app = 'deposits'
concept = 'aptrentaldeposit'


class AptRentalDepositActionViewTest(test_views.ConceptActionsViewTest):

    app = app
    concept = concept


class AptRentalDepositNewViewTest(test_views.ConceptNewViewTest):

    app = app
    concept = concept


class AptRentalDepositDeleteViewTest(test_views.ConceptDeleteViewTest):

    app = app
    concept = concept


class AptRentalDepositDetailViewTest(test_views.ConceptDetailViewTest):

    app = app
    concept = concept


class AptRentalDepositEditlViewTest(test_views.ConceptEditViewTest):

    app = app
    concept = concept


class AptRentalDepositRowViewTest(test_views.ConceptRowViewTest):

    app = app
    concept = concept


class DepositDueTodayViewTest(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_permission = 'deposits.add_depositreturn'
        cls.url = 'deposits_due_today'
        cls.kwargs = {}
        cls.referer = '/'
        cls.get_template = 'concepts/concept_list.html'
        cls.get_url = reverse('concept_list')


"""
For future use

class DepositListViewTest(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_permission = ''
        cls.url = 'deposit_list'
        cls.kwargs = {}
        cls.referer = '/'
        cls.get_template = 'concepts/concept_list.html'
        
"""

app = 'deposits'
concept = 'depositreturn'


class DepositreturnActionViewTest(test_views.ConceptActionsViewTest):

    app = app
    concept = concept


class DepositreturnNewViewTest(test_views.ConceptNewViewTest):

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
        aptrentaldeposit = model_creation.create_test_aptrentaldeposit(transaction, aptrental, timezone.now())
        transaction.close(self.admin)
        self.kwargs = {'concept_code': aptrentaldeposit.code}
        self.get_url = 'pass'
        self.get_template = 'transactions/transaction_edit.html'
        self.repeat_get()

    def test_with_concept_and_transaction(self):
        # Create a deposit
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        aptrentaldeposit = model_creation.create_test_aptrentaldeposit(transaction, aptrental, timezone.now())
        transaction.close(self.admin)
        self.kwargs = {
            'concept_code': aptrentaldeposit.code,
        }
        if self.client.session:  # pragma: no cover
            session = self.client.session
        else:  # pragma: no cover
            engine = import_module(settings.SESSION_ENGINE)
            session = engine.SessionStore()
        session['depositreturn_transaction_code'] = create_test_transaction(self.admin, timezone.now()).code
        session.save()
        self.get_url = 'pass'
        self.get_template = 'transactions/transaction_edit.html'
        self.repeat_get()

    def test_with_nonreturnable_concept(self):
        # Create a deposit
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        aptrentaldeposit = model_creation.create_test_aptrentaldeposit(transaction, aptrental, timezone.now())
        self.kwargs = {'concept_code': aptrentaldeposit.code}
        self.get_url = 'pass'
        self.get_template = 'core/message.html'
        self.repeat_get()


class DepositreturnDeleteViewTest(test_views.ConceptDeleteViewTest):

    app = app
    concept = concept


class DepositreturnDetailViewTest(test_views.ConceptDetailViewTest):

    app = app
    concept = concept


class DepositreturnRowViewTest(test_views.ConceptRowViewTest):

    app = app
    concept = concept

