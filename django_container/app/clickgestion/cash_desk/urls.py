from clickgestion.cash_desk.forms import CashFloatDepositForm, CashFloatWithdrawalForm
from clickgestion.concepts.views import concept_delete, concept_detail, concept_edit
from clickgestion.core.utilities import custom_permission_required
from django.conf.urls import url
from clickgestion.cash_desk import views

urlpatterns = [
    url(r'^balance/$', views.cash_desk_balance, name='cash_desk_balance'),
    url(r'^close/$', views.cash_desk_close, name='cash_desk_close'),
    url(r'^closures/$', views.CashCloseList.as_view(), name='cashclose_list'),
    url(r'^closures/(?P<cashclose_code>CC[A-F0-9]+)/$', views.cashclose_row, name='cashclose_row'),
    url(r'^closures/(?P<cashclose_code>CC[A-F0-9]+)/detail/$', views.cashclose_detail, name='cashclose_detail'),
    url(r'^closures/(?P<cashclose_code>CC[A-F0-9]+)/document/$', views.cashclose_document, name='cashclose_document'),
    url(r'^deposits/new/(?P<transaction_code>T[A-F0-9]{10})$',
        custom_permission_required('cash_desk.add_cashfloatdeposit')(concept_edit),
        {'concept_form': CashFloatDepositForm},
        name='cashfloatdeposit_new'),
    url(r'^deposits/(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)$',
        custom_permission_required('cash_desk.add_cashfloatdeposit')(concept_detail),
        {'concept_form': CashFloatDepositForm},
        name='cashfloatdeposit_detail'),
    url(r'^deposits/(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/edit/$',
        custom_permission_required('cash_desk.add_cashfloatdeposit')(concept_edit),
        {'concept_form': CashFloatDepositForm},
        name='cashfloatdeposit_edit'),
    url(r'^deposits/(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/delete/$',
        custom_permission_required('cash_desk.add_cashfloatdeposit')(concept_delete),
        {'concept_form': CashFloatDepositForm},
        name='cashfloatdeposit_delete'),

    url(r'^withdrawals/new/(?P<transaction_code>T[A-F0-9]{10})$',
        custom_permission_required('cash_desk.add_cashfloatwithdrawal')(concept_edit),
        {'concept_form': CashFloatWithdrawalForm},
        name='cashfloatwithdrawal_new'),
    url(r'^withdrawals/(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)$',
        custom_permission_required('cash_desk.add_cashfloatwithdrawal')(concept_detail),
        {'concept_form': CashFloatWithdrawalForm},
        name='cashfloatwithdrawal_detail'),
    url(r'^withdrawals/(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/edit/$',
        custom_permission_required('cash_desk.add_cashfloatwithdrawal')(concept_edit),
        {'concept_form': CashFloatWithdrawalForm},
        name='cashfloatwithdrawal_edit'),
    url(r'^withdrawal/(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/delete/$',
        custom_permission_required('cash_desk.add_cashfloatwithdrawal')(concept_delete),
        {'concept_form': CashFloatWithdrawalForm},
        name='cashfloatwithdrawal_delete'),
]
