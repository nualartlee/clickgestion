from django.conf.urls import url
from clickgestion.deposits import views
from clickgestion.deposits.forms import AptRentalDepositForm
from clickgestion.concepts.views import concept_delete, concept_detail, concept_edit

urlpatterns = [

    url(r'^$', views.DepositList.as_view(),
        name='deposit_list'),

    url(r'^aptrental/new/(?P<transaction_code>T[A-F0-9]{10})$', concept_edit,
        {'concept_form': AptRentalDepositForm},
        name='aptrentaldeposit_new'),
    url(r'^aptrental/(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)$', concept_detail,
        {'concept_form': AptRentalDepositForm},
        name='aptrentaldeposit_detail'),
    url(r'^aptrental/(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/edit/$', concept_edit,
        {'concept_form': AptRentalDepositForm},
        name='aptrentaldeposit_edit'),
    url(r'^aptrental/(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/delete/$', concept_delete,
        {'concept_form': AptRentalDepositForm},
        name='aptrentaldeposit_delete'),

    url(r'^returns/(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/$', views.depositreturn_detail,
        name='depositreturn_detail'),
    url(r'^returns/new/(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/$', views.depositreturn_new,
        name='depositreturn_new'),
    url(r'^returns/new/(?P<transaction_code>T[A-F0-9]{10})/$', views.depositreturn_new,
        name='depositreturn_new'),
    url(r'^returns/today$', views.depositreturns_today,
        name='depositreturns_today'),
]
