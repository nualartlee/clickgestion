from django.conf.urls import url
from clickgestion.transactions import views

urlpatterns = [
    url(r'^$', views.TransactionList.as_view(), name='transaction_list'),
    url(r'^new/$', views.transaction_new, name='transaction_new'),
    url(r'^(?P<transaction_id>[0-9]+)/$', views.transaction_detail,
        name='transaction_detail'),
    url(r'^(?P<transaction_id>[0-9]+)/edit/$', views.transaction_edit,
        name='transaction_edit'),
    url(r'^(?P<transaction_id>[0-9]+)/pay/$', views.transaction_pay,
        name='transaction_pay'),
]
