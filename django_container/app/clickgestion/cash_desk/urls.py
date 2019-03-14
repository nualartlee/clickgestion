from django.conf.urls import url
from clickgestion.cash_desk import views
from clickgestion.concepts.views import concept_delete, concept_detail, concept_edit
from clickgestion.cash_desk.forms import CashFloatDepositForm, CashFloatWithdrawalForm

urlpatterns = [
    url(r'^balance/$', views.cash_desk_balance, name='cash_desk_balance'),
    url(r'^close/$', views.cash_desk_close, name='cash_desk_close'),
    url(r'^closures/$', views.CashCloseList.as_view(), name='cashclose_list'),
    url(r'^closures/(?P<cashclose_code>CC[A-F0-9]+)/$', views.cashclose_row, name='cashclose_row'),
    url(r'^closures/(?P<cashclose_code>CC[A-F0-9]+)/detail/$', views.cashclose_detail, name='cashclose_detail'),
    url(r'^closures/(?P<cashclose_code>CC[A-F0-9]+)/document/$', views.cashclose_document, name='cashclose_document'),
    url(r'^deposits/new/(?P<transaction_code>T[A-F0-9]{10})$', concept_edit, {'concept_form': CashFloatDepositForm},
        name='cashfloat_deposit_new'),
    url(r'^deposits/(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)$', concept_detail, {'concept_form': CashFloatDepositForm},
        name='cashfloat_deposit_detail'),
    url(r'^deposits/(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/edit/$', concept_edit, {'concept_form': CashFloatDepositForm},
        name='cashfloat_deposit_edit'),
    url(r'^deposits/(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/delete/$', concept_delete, {'concept_form': CashFloatDepositForm},
        name='cashfloat_deposit_delete'),

    url(r'^withdrawals/new/(?P<transaction_code>T[A-F0-9]{10})$', concept_edit, {'concept_form': CashFloatWithdrawalForm},
        name='cashfloat_withdrawal_new'),
    url(r'^withdrawals/(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)$', concept_detail, {'concept_form': CashFloatWithdrawalForm},
        name='cashfloat_withdrawal_detail'),
    url(r'^withdrawals/(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/edit/$', concept_edit, {'concept_form': CashFloatWithdrawalForm},
        name='cashfloat_withdrawal_edit'),
    url(r'^withdrawal/(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/delete/$', concept_delete, {'concept_form': CashFloatWithdrawalForm},
        name='cashfloat_withdrawal_delete'),
]
