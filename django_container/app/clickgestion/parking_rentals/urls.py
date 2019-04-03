from clickgestion.parking_rentals.forms import ParkingRentalForm
from clickgestion.concepts.views import concept_delete, concept_detail, concept_edit
from clickgestion.core.utilities import custom_permission_required
from django.conf.urls import url

urlpatterns = [
    url(r'^new/(?P<transaction_code>T[A-F0-9]{10})$',
        custom_permission_required('parking_rentals.add_parkingrental')(concept_edit),
        {'concept_form': ParkingRentalForm},
        name='parkingrental_new'),
    url(r'^(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)$',
        custom_permission_required('parking_rentals.add_parkingrental')(concept_detail),
        {'concept_form': ParkingRentalForm},
        name='parkingrental_detail'),
    url(r'^(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/edit/$',
        custom_permission_required('parking_rentals.add_parkingrental')(concept_edit),
        {'concept_form': ParkingRentalForm},
        name='parkingrental_edit'),
    url(r'^(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/delete/$',
        custom_permission_required('parking_rentals.add_parkingrental')(concept_delete),
        {'concept_form': ParkingRentalForm},
        name='parkingrental_delete'),
]
