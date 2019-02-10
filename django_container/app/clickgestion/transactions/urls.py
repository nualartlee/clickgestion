from django.conf.urls import url
from clickgestion.transactions import views

urlpatterns = [
    url(r'^(?P<transaction_id>[0-9]+)/edit/$', views.transaction_edit,
        name='transaction_edit'),
    url(r'^new/$', views.transaction_new, name='transaction_new'),
]
