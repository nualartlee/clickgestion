from django.conf.urls import url
from clickgestion.deposit_returns import views

urlpatterns = [
    url(r'^(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/$', views.deposit_return,
        name='deposit_return'),
    url(r'^new/(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/$', views.deposit_return_new,
        name='deposit_return_new'),
    url(r'^new/(?P<transaction_code>T[A-F0-9]{10})/$', views.deposit_return_new,
        name='deposit_return_new'),
    url(r'^today$', views.today, name='deposit_returns_today'),
]
