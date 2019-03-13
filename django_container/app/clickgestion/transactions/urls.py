from django.conf.urls import url
from clickgestion.transactions import views

urlpatterns = [
    url(r'^$', views.TransactionList.as_view(), name='transaction_list'),
    url(r'^new/$', views.transaction_edit, {'transaction_code': None}, name='transaction_new'),
    url(r'^open/$', views.transactions_open, name='transactions_open'),
    url(r'^(?P<transaction_code>T[A-F0-9]+)/$', views.transaction_row,
        name='transaction_row'),
    url(r'^(?P<transaction_code>T[A-F0-9]+)/actions/$', views.transaction_actions,
        name='transaction_actions'),
    url(r'^(?P<transaction_code>T[A-F0-9]+)/concepts/$', views.transaction_concepts,
        name='transaction_concepts'),
    url(r'^(?P<transaction_code>T[A-F0-9]+)/detail/$', views.transaction_detail,
        name='transaction_detail'),
    url(r'^(?P<transaction_code>T[A-F0-9]+)/delete/$', views.transaction_delete,
        name='transaction_delete'),
    url(r'^(?P<transaction_code>T[A-F0-9]+)/document/$', views.transaction_document,
        name='transaction_document'),
    url(r'^(?P<transaction_code>T[A-F0-9]+)/edit/$', views.transaction_edit,
        name='transaction_edit'),
    url(r'^(?P<transaction_code>T[A-F0-9]+)/pay/$', views.transaction_pay,
        name='transaction_pay'),
]
