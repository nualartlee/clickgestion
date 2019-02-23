from django.conf.urls import url
from clickgestion.apt_rentals import views
from clickgestion.transactions.views import concept_edit, concept_delete
from clickgestion.apt_rentals.models import AptRentalDeposit

urlpatterns = [
    url(r'^new/(?P<transaction_code>T[A-F0-9]+)$', views.rental_new,
        name='rental_new'),
    url(r'^(?P<rental_id>[0-9]+)$', views.rental_detail,
        name='rental_detail'),
    url(r'^(?P<rental_id>[0-9]+)/edit/$', views.rental_edit,
        name='rental_edit'),
    url(r'^(?P<rental_id>[0-9]+)/delete/$', views.rental_delete,
        name='rental_delete'),

    url(r'^deposits/new/(?P<transaction_code>T[A-F0-9]+)$', concept_edit, {'concept_class': AptRentalDeposit},
        name='deposit_new'),
    url(r'^deposits/(?P<concept_code>T[-A-F0-9]+)$', views.deposit_detail,
        name='deposit_detail'),
    url(r'^deposits/(?P<concept_code>T[-A-F0-9]+)/edit/$', concept_edit, {'concept_class': AptRentalDeposit},
        name='deposit_edit'),
    url(r'^deposits/(?P<concept_code>T[-A-Z0-9]+)/delete/$', concept_delete, {'concept_class': AptRentalDeposit},
        name='deposit_delete'),
]
