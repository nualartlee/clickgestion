from clickgestion.deposits.forms import AptRentalDepositForm, DepositReturnForm
from clickgestion.concepts.views import concept_delete, concept_detail, concept_edit
from clickgestion.core.utilities import custom_permission_required
from clickgestion.deposits import views
from django.conf.urls import url

urlpatterns = [

    url(r'^$', views.DepositList.as_view(),
        name='deposit_list'),

    url(r'^aptrental/new/(?P<transaction_code>T[A-F0-9]{10})$',
        custom_permission_required('deposits.add_aptrentaldeposit')(concept_edit),
        {'concept_form': AptRentalDepositForm},
        name='aptrentaldeposit_new'),
    url(r'^aptrental/(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)$',
        custom_permission_required('deposits.add_aptrentaldeposit')(concept_detail),
        {'concept_form': AptRentalDepositForm},
        name='aptrentaldeposit_detail'),
    url(r'^aptrental/(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/edit/$',
        custom_permission_required('deposits.add_aptrentaldeposit')(concept_edit),
        {'concept_form': AptRentalDepositForm},
        name='aptrentaldeposit_edit'),
    url(r'^aptrental/(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/delete/$',
        custom_permission_required('deposits.add_aptrentaldeposit')(concept_delete),
        {'concept_form': AptRentalDepositForm},
        name='aptrentaldeposit_delete'),

    url(r'^returns/(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/$',
        custom_permission_required('deposits.add_depositreturn')(concept_detail),
        {'concept_form': DepositReturnForm},
        name='depositreturn_detail'),
    url(r'^returns/(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/delete/$',
        custom_permission_required('deposits.add_depositreturn')(concept_delete),
        {'concept_form': DepositReturnForm},
        name='depositreturn_delete'),
    url(r'^returns/new/(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/$',
        custom_permission_required('deposits.add_depositreturn')(views.depositreturn_new),
        name='depositreturn_new'),
    url(r'^returns/new/(?P<transaction_code>T[A-F0-9]{10})/$',
        custom_permission_required('deposits.add_depositreturn')(views.depositreturn_new),
        name='depositreturn_new'),
    url(r'^returns/today$',
        custom_permission_required('deposits.add_depositreturn')(views.depositreturns_today),
        name='depositreturns_today'),
]
