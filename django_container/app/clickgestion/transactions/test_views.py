from clickgestion.core.test import CustomTestCase, CustomViewTestCase
from clickgestion.transactions.views import get_available_concepts
from importlib import import_module
from clickgestion.core import model_creation
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from clickgestion.transactions.models import Transaction


class TestGetAvailableConcepts(CustomTestCase):

    def test_ok(self):
        assert get_available_concepts(self.admin, self.transaction)

    def test_empty_transaction(self):
        transaction = Transaction()
        cn = get_available_concepts(self.admin, transaction)
        self.assertGreater(len(cn), 0)
        # None should be disabled
        for c in cn:
            self.assertEqual(c['disabled'], False)

    def test_transaction_with_rental(self):
        date = timezone.now()
        employee = model_creation.get_sales_employee()
        transaction = model_creation.create_test_client_transaction(employee, date)
        aptrental = model_creation.create_test_aptrental(transaction, date)
        transaction.closed = True
        transaction.closed_date = date
        transaction.save()
        cn = get_available_concepts(self.admin, transaction)
        self.assertGreater(len(cn), 0)
        # Cash operations should be disabled
        for c in cn:
            if c['name'] in ['Cash Float Deposit', 'Cash Float Withdrawal']:
                self.assertEqual(c['disabled'], True, msg='{} is not disabled'.format(c['name']))
            else:
                self.assertEqual(c['disabled'], False, msg='{} is not enabled'.format(c['name']))


class TestTransactionActionsView(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_permission = ''
        cls.url = 'transaction_actions'
        cls.kwargs = {'transaction_code': cls.transaction.code}
        cls.referer = '/'
        cls.get_template = 'transactions/transaction_actions.html'


class TestTransactionConceptsView(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_permission = ''
        cls.url = 'transaction_concepts'
        cls.kwargs = {'transaction_code': cls.transaction.code}
        cls.referer = '/'
        cls.get_template = 'concepts/concept_list.html'
        cls.get_url = reverse('concept_list')


class TestTransactionDeleteView(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_permission = 'transactions.add_transaction'
        cls.url = 'transaction_delete'
        cls.kwargs = {'transaction_code': cls.transaction.code}
        cls.referer = '/'
        cls.get_template = 'core/delete.html'

    def test_closed(self):
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        aptrentaldeposit = model_creation.create_test_aptrentaldeposit(transaction, aptrental, timezone.now())
        transaction.close(self.admin)
        self.kwargs = {'transaction_code': transaction.code}
        self.log_admin_in()
        response = self.client.get(
            reverse(self.url, kwargs=self.kwargs),
            follow=True,
        )
        self.assertTemplateUsed(response, 'core/message.html')
        self.assertEqual(response.status_code, 200)

    def test_post_ok(self):
        self.log_admin_in()
        response = self.client.post(
            reverse(self.url, kwargs=self.kwargs),
            follow=True, HTTP_REFERER='/',
        )
        self.assertTemplateUsed(response, 'transactions/transaction_list.html')
        self.assertEqual(response.status_code, 200)

    def test_post_with_session_data(self):
        if self.client.session:  # pragma: no cover
            session = self.client.session
        else:  # pragma: no cover
            engine = import_module(settings.SESSION_ENGINE)
            session = engine.SessionStore()
        session['refund_transaction_code'] = self.transaction.code
        session['depositreturn_transaction_code'] = self.transaction.code
        session.save()
        self.log_admin_in()
        response = self.client.post(
            reverse(self.url, kwargs=self.kwargs),
            follow=True, HTTP_REFERER='/',
        )
        self.assertTemplateUsed(response, 'transactions/transaction_list.html')
        self.assertEqual(response.status_code, 200)


class TestTransactionDetailView(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_permission = ''
        cls.url = 'transaction_detail'
        cls.transaction.close(cls.admin)
        cls.kwargs = {'transaction_code': cls.transaction.code}
        cls.referer = '/'
        cls.get_template = 'transactions/transaction_detail.html'

    def test_open_transaction(self):
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        self.kwargs = {'transaction_code': transaction.code}
        self.get_url = 'pass'
        self.get_template = 'transactions/transaction_edit.html'
        self.repeat_get()


class TestTransactionDocumentView(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_permission = ''
        cls.url = 'transaction_document'
        cls.kwargs = {'transaction_code': cls.transaction.code}
        cls.referer = '/'
        cls.get_template = 'transactions/transaction_document.html'


class TestTransactionEditView(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_permission = ''
        cls.url = 'transaction_edit'
        cls.kwargs = {'transaction_code': cls.transaction.code}
        cls.referer = '/'
        cls.get_template = 'transactions/transaction_edit.html'

    def test_closed(self):
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        aptrentaldeposit = model_creation.create_test_aptrentaldeposit(transaction, aptrental, timezone.now())
        transaction.close(self.admin)
        self.kwargs = {'transaction_code': transaction.code}
        self.log_admin_in()
        response = self.client.get(
            reverse(self.url, kwargs=self.kwargs),
            follow=True,
        )
        self.assertTemplateUsed(response, 'core/message.html')
        self.assertEqual(response.status_code, 200)

    def test_post_cancel_button(self):
        self.log_admin_in()
        response = self.client.post(
            reverse(self.url, kwargs=self.kwargs),
            {'cancel_button': True},
            follow=True,
        )
        self.assertTemplateUsed(response, 'core/index.html')
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Transaction.DoesNotExist):
            Transaction.objects.get(code=self.transaction.code)

    def test_post_pay_button(self):
        self.log_admin_in()
        post_data = {
            'pay_button': True,
            'cancel_button': False,
        }
        response = self.client.post(
            reverse(self.url, kwargs=self.kwargs),
            post_data,
            follow=True,
        )
        self.assertTemplateUsed(response, 'transactions/transaction_pay.html')
        self.assertEqual(response.status_code, 200)

    def test_post_save_button(self):
        self.log_admin_in()
        post_data = {
            'cancel_button': False,
            'pay_button': False,
            'save_button': True,
        }
        response = self.client.post(
            reverse(self.url, kwargs=self.kwargs),
            post_data,
            follow=True,
        )
        self.assertTemplateUsed(response, 'transactions/transaction_list.html')
        self.assertEqual(response.status_code, 200)


class TestTransactionListView(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_permission = ''
        cls.url = 'transaction_list'
        cls.kwargs = {}
        cls.referer = '/'
        cls.get_template = 'transactions/transaction_list.html'


class TestTransactionNewView(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_permission = ''
        cls.url = 'transaction_new'
        cls.kwargs = {}
        cls.referer = '/'
        cls.get_template = 'transactions/transaction_edit.html'
        cls.get_url = 'pass'


class TestTransactionPayView(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_permission = ''
        cls.url = 'transaction_pay'
        cls.kwargs = {'transaction_code': cls.transaction.code}
        cls.referer = '/'
        cls.get_template = 'transactions/transaction_pay.html'

    def test_closed(self):
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        aptrentaldeposit = model_creation.create_test_aptrentaldeposit(transaction, aptrental, timezone.now())
        transaction.close(self.admin)
        self.kwargs = {'transaction_code': transaction.code}
        self.log_admin_in()
        response = self.client.get(
            reverse(self.url, kwargs=self.kwargs),
            follow=True,
        )
        self.assertTemplateUsed(response, 'core/message.html')
        self.assertEqual(response.status_code, 200)

    def test_bad(self):
        transaction = model_creation.create_test_transaction(self.admin, timezone.now())
        aptrental = model_creation.create_test_aptrental(transaction, timezone.now())
        transaction.apt_number = None
        transaction.client_first_name = None
        transaction.client_last_name = None
        transaction.client_id = None
        transaction.save()
        self.kwargs = {'transaction_code': transaction.code}

        post_data = {
            'confirm_button': True,
            'cancel_button': False,
        }
        self.log_admin_in()
        response = self.client.post(
            reverse(self.url, kwargs=self.kwargs),
            post_data,
            follow=True,
        )
        self.assertTemplateUsed(response, self.get_template)
        self.assertEqual(response.status_code, 200)

    def test_post_confirm_button(self):
        self.log_admin_in()
        post_data = {
            'confirm_button': True,
            'cancel_button': False,
            'client_apt_number': '1605',
            'client_first_name': 'Donna',
            'client_last_name': 'Kavanagh',
            'client_id': 'AATEST'
        }
        response = self.client.post(
            reverse(self.url, kwargs=self.kwargs),
            post_data,
            follow=True,
        )
        self.assertTemplateUsed(response, 'transactions/transaction_detail.html')
        self.assertEqual(response.status_code, 200)

    def test_post_save_button(self):
        self.log_admin_in()
        post_data = {
            'save_button': True,
            'cancel_button': False,
            'client_apt_number': '1605',
            'client_first_name': 'Donna',
            'client_last_name': 'Kavanagh',
            'client_id': 'AATEST'
        }
        response = self.client.post(
            reverse(self.url, kwargs=self.kwargs),
            post_data,
            follow=True,
        )
        self.assertTemplateUsed(response, 'transactions/transaction_list.html')
        self.assertEqual(response.status_code, 200)

    def test_post_cancel_button(self):
        self.log_admin_in()
        response = self.client.post(
            reverse(self.url, kwargs=self.kwargs),
            {'cancel_button': True},
            follow=True,
        )
        self.assertTemplateUsed(response, 'core/index.html')
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Transaction.DoesNotExist):
            Transaction.objects.get(code=self.transaction.code)


class TestTransactionsOpenView(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_permission = ''
        cls.url = 'transaction_list'
        cls.kwargs = {}
        cls.referer = '/'
        cls.get_template = 'transactions/transaction_list.html'


class TestTransactionRowView(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_permission = ''
        cls.url = 'transaction_row'
        cls.kwargs = {'transaction_code': cls.transaction.code}
        cls.referer = '/'
        cls.get_template = 'transactions/transaction_list.html'
        cls.get_url = reverse('transaction_list')

