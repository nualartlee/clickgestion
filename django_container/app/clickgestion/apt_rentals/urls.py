from clickgestion.apt_rentals.forms import AptRentalForm
from clickgestion.concepts.views import concept_delete, concept_detail, concept_edit
from clickgestion.core.utilities import custom_permission_required
from django.conf.urls import url

urlpatterns = [
    url(r'^new/(?P<transaction_code>T[A-F0-9]{10})$',
        custom_permission_required('apt_rentals.add_aptrental')(concept_edit),
        {'concept_form': AptRentalForm},
        name='aptrental_new'),
    url(r'^(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)$',
        custom_permission_required('apt_rentals.add_aptrental')(concept_detail),
        {'concept_form': AptRentalForm},
        name='aptrental_detail'),
    url(r'^(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/edit/$',
        custom_permission_required('apt_rentals.add_aptrental')(concept_edit),
        {'concept_form': AptRentalForm},
        name='aptrental_edit'),
    url(r'^(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/delete/$',
        custom_permission_required('apt_rentals.add_aptrental')(concept_delete),
        {'concept_form': AptRentalForm},
        name='aptrental_delete'),
]
