from django.conf.urls import url, include
from clickgestion.cash_desk import views
from clickgestion.transactions.views import concept_delete, concept_detail, concept_edit
from clickgestion.cash_desk.forms import CashFloatDepositForm, CashFloatWithdrawalForm

urlpatterns = [
    url(r'^balance/$', views.cash_balance, name='cash_balance'),
    url(r'^close/$', views.cash_close, name='cash_close'),
    #url(r'^float/', include('clickgestion.cash_float.urls')),
    url(r'^deposits/new/(?P<transaction_code>T[A-F0-9]+)$', concept_edit, {'concept_form': CashFloatDepositForm},
        name='cashfloat_deposit_new'),
    url(r'^deposits/(?P<concept_code>T[-A-Z0-9]+)$', concept_detail, {'concept_form': CashFloatDepositForm},
        name='cashfloat_deposit_detail'),
    url(r'^deposits/(?P<concept_code>T[-A-Z0-9]+)/edit/$', concept_edit, {'concept_form': CashFloatDepositForm},
        name='cashfloat_deposit_edit'),
    url(r'^deposits/(?P<concept_code>T[-A-Z0-9]+)/delete/$', concept_delete, {'concept_form': CashFloatDepositForm},
        name='cashfloat_deposit_delete'),

    url(r'^withdrawals/new/(?P<transaction_code>T[A-F0-9]+)$', concept_edit, {'concept_form': CashFloatWithdrawalForm},
        name='cashfloat_withdrawal_new'),
    url(r'^withdrawals/(?P<concept_code>T[-A-Z0-9]+)$', concept_detail, {'concept_form': CashFloatWithdrawalForm},
        name='cashfloat_withdrawal_detail'),
    url(r'^withdrawals/(?P<concept_code>T[-A-Z0-9]+)/edit/$', concept_edit, {'concept_form': CashFloatWithdrawalForm},
        name='cashfloat_withdrawal_edit'),
    url(r'^withdrawal/(?P<concept_code>T[-A-Z0-9]+)/delete/$', concept_delete, {'concept_form': CashFloatWithdrawalForm},
        name='cashfloat_withdrawal_delete'),
]
