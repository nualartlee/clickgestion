from clickgestion.core.test import CustomTestCase, CustomViewTestCase


class TestCashFloatDepositNewView(CustomTestCase, CustomViewTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_get = True
        cls.required_access_level = 1
        cls.url = 'cash_float_deposit_new'
        cls.kwargs = {'transaction_code': cls.transaction.code}
        cls.referer = '/'
        cls.get_template = 'transactions/concept_new.html'



#class TestTransactionEditView(CustomTestCase, CustomViewTestCase):
#
#    @classmethod
#    def setUpTestData(cls):
#        super().setUpTestData()
#        cls.test_get = True
#        cls.required_access_level = 1
#        cls.url = 'transaction_edit'
#        cls.kwargs = {'transaction_code': cls.transaction.code}
#        cls.referer = '/'
#        cls.get_template = 'transactions/transaction_edit.html'
#
#    def test_post_pay_button(self):
#        self.log_admin_in()
#        post_data = {
#            'pay_button': True,
#            'cancel_button': False,
#        }
#        response = self.client.post(
#            reverse(self.url, kwargs=self.kwargs),
#            post_data,
#            follow=True,
#        )
#        self.assertTemplateUsed(response, 'transactions/transaction_pay.html')
#        self.assertEqual(response.status_code, 200)
#
#    def test_post_cancel_button(self):
#        self.log_admin_in()
#        response = self.client.post(
#            reverse(self.url, kwargs=self.kwargs),
#            {'cancel_button': True,},
#            follow=True,
#        )
#        self.assertTemplateUsed(response, 'core/index.html')
#        self.assertEqual(response.status_code, 200)
#        with self.assertRaises(Transaction.DoesNotExist):
#            Transaction.objects.get(code=self.transaction.code)
#
#
#class TestTransactionPayView(CustomTestCase, CustomViewTestCase):
#
#    @classmethod
#    def setUpTestData(cls):
#        super().setUpTestData()
#        cls.test_get = True
#        cls.required_access_level = 1
#        cls.url = 'transaction_pay'
#        cls.kwargs = {'transaction_code': cls.transaction.code}
#        cls.referer = '/'
#        cls.get_template = 'transactions/transaction_pay.html'
#
#    def test_post_confirm_button(self):
#        self.log_admin_in()
#        post_data = {
#            'save_button': True,
#            'cancel_button': False,
#            'client_apt_number': '1605',
#            'client_first_name': 'Donna',
#            'client_last_name': 'Kavanagh',
#            'client_id': 'AATEST'
#        }
#        response = self.client.post(
#            reverse(self.url, kwargs=self.kwargs),
#            post_data,
#            follow=True,
#        )
#        self.assertTemplateUsed(response, 'transactions/transaction_detail.html')
#        self.assertEqual(response.status_code, 200)
#
#    def test_post_save_button(self):
#        self.log_admin_in()
#        post_data = {
#            'save_button': True,
#            'cancel_button': False,
#            'client_apt_number': '1605',
#            'client_first_name': 'Donna',
#            'client_last_name': 'Kavanagh',
#            'client_id': 'AATEST'
#        }
#        response = self.client.post(
#            reverse(self.url, kwargs=self.kwargs),
#            post_data,
#            follow=True,
#        )
#        self.assertTemplateUsed(response, 'transactions/transaction_detail.html')
#        self.assertEqual(response.status_code, 200)
#
#    def test_post_cancel_button(self):
#        self.log_admin_in()
#        response = self.client.post(
#            reverse(self.url, kwargs=self.kwargs),
#            {'cancel_button': True,},
#            follow=True,
#        )
#        self.assertTemplateUsed(response, 'core/index.html')
#        self.assertEqual(response.status_code, 200)
#        with self.assertRaises(Transaction.DoesNotExist):
#            Transaction.objects.get(code=self.transaction.code)
#
