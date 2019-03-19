from django.urls import reverse
from clickgestion.core.test import CustomTestCase, CustomViewTestCase
from clickgestion.core.model_creation import create_test_models
from clickgestion.cash_desk.models import CashClose
from clickgestion.concepts import test_views


class TestCashDeskBalanceView(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        print('creating test models')
        create_test_models(days=7)
        cls.test_get = True
        cls.required_permission = ''
        cls.url = 'cash_desk_balance'
        cls.kwargs = {}
        cls.referer = '/'
        cls.get_template = 'cash_desk/cashclose_detail.html'


class TestCashDeskCloseView(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        print('creating test models')
        create_test_models(days=1)
        cls.test_get = True
        cls.required_permission = 'cash_desk.add_cashclose'
        cls.url = 'cash_desk_close'
        cls.kwargs = {}
        cls.referer = '/'
        cls.get_template = 'cash_desk/cash_desk_close.html'

    def test_post_ok(self):
        self.log_admin_in()
        response = self.client.post(
            reverse(self.url, kwargs=self.kwargs),
            follow=True,
        )
        self.assertTemplateUsed(response, 'core/message.html')
        self.assertEqual(response.status_code, 200)


class TestCashcloseDetailView(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        print('creating test models')
        create_test_models(days=2)
        cls.test_get = True
        cls.required_permission = 'cash_desk.add_cashclose'
        cls.url = 'cashclose_detail'
        cls.kwargs = {'cashclose_code': CashClose.objects.first().code}
        cls.referer = '/'
        cls.get_template = 'cash_desk/cashclose_detail.html'


class TestCashcloseDocumentView(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        print('creating test models')
        create_test_models(days=2)
        cls.test_get = True
        cls.required_permission = 'cash_desk.add_cashclose'
        cls.url = 'cashclose_document'
        cls.kwargs = {'cashclose_code': CashClose.objects.first().code}
        cls.referer = '/'
        cls.get_template = 'cash_desk/cashclose_document_a4.html'


class TestCashCloseRowView(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        print('creating test models')
        create_test_models(days=1)
        cls.test_get = True
        cls.required_permission = 'cash_desk.add_cashclose'
        cls.url = 'cashclose_row'
        cls.kwargs = {'cashclose_code': CashClose.objects.first().code}
        cls.referer = '/'
        cls.get_template = 'cash_desk/cashclose_list.html'
        cls.get_url = reverse('cashclose_list')


class TestCashCloseListView(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        print('creating test models')
        create_test_models(days=1)
        cls.test_get = True
        cls.required_permission = 'cash_desk.add_cashclose'
        cls.url = 'cashclose_list'
        cls.kwargs = {}
        cls.referer = '/'
        cls.get_template = 'cash_desk/cashclose_list.html'


app = 'cash_desk'
concept = 'cashfloatdeposit'


class CashFloatDepositActionViewTest(test_views.ConceptActionsViewTest):

    app = app
    concept = concept


class CashFloatDepositNewViewTest(test_views.ConceptNewViewTest):

    app = app
    concept = concept


class CashFloatDepositDeleteViewTest(test_views.ConceptDeleteViewTest):

    app = app
    concept = concept


class CashFloatDepositDetailViewTest(test_views.ConceptDetailViewTest):

    app = app
    concept = concept


class CashFloatDepositEditViewTest(test_views.ConceptEditViewTest):

    app = app
    concept = concept


class CashFloatDepositRowViewTest(test_views.ConceptRowViewTest):

    app = app
    concept = concept


app = 'cash_desk'
concept = 'cashfloatwithdrawal'


class CashFloatWithdrawalActionViewTest(test_views.ConceptActionsViewTest):

    app = app
    concept = concept


class CashFloatWithdrawalNewViewTest(test_views.ConceptNewViewTest):

    app = app
    concept = concept


class CashFloatWithdrawalDeleteViewTest(test_views.ConceptDeleteViewTest):

    app = app
    concept = concept


class CashFloatWithdrawalDetailViewTest(test_views.ConceptDetailViewTest):

    app = app
    concept = concept


class CashFloatWithdrawalEditViewTest(test_views.ConceptEditViewTest):

    app = app
    concept = concept


class CashFloatWithdrawalRowViewTest(test_views.ConceptEditViewTest):

    app = app
    concept = concept
