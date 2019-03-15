from django.conf.urls import url
from clickgestion.concepts.views import concept_delete, concept_detail, concept_edit
from clickgestion.apt_rentals.forms import AptRentalForm

urlpatterns = [
    url(r'^new/(?P<transaction_code>T[A-F0-9]{10})$', concept_edit, {'concept_form': AptRentalForm},
        name='rental_new'),
    url(r'^(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)$', concept_detail, {'concept_form': AptRentalForm},
        name='rental_detail'),
    url(r'^(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/edit/$', concept_edit, {'concept_form': AptRentalForm},
        name='rental_edit'),
    url(r'^(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/delete/$', concept_delete, {'concept_form': AptRentalForm},
        name='rental_delete'),
]
