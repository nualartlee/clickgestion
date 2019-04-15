from clickgestion.service_sales.forms import ServiceSalesForm
from clickgestion.concepts.views import concept_delete, concept_detail, concept_edit
from clickgestion.core.utilities import custom_permission_required
from django.conf.urls import url

urlpatterns = [
    url(r'^new/(?P<transaction_code>T[A-F0-9]{10})$',
        custom_permission_required('service_sales.add_servicesale')(concept_edit),
        {'concept_form': ServiceSalesForm},
        name='servicesale_new'),
    url(r'^(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)$',
        custom_permission_required('service_sales.add_servicesale')(concept_detail),
        {'concept_form': ServiceSalesForm},
        name='servicesale_detail'),
    url(r'^(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/edit/$',
        custom_permission_required('service_sales.add_servicesale')(concept_edit),
        {'concept_form': ServiceSalesForm},
        name='servicesale_edit'),
    url(r'^(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/delete/$',
        custom_permission_required('service_sales.add_servicesale')(concept_delete),
        {'concept_form': ServiceSalesForm},
        name='servicesale_delete'),
]
