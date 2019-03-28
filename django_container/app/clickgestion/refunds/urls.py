from clickgestion.refunds.forms import RefundForm
from clickgestion.concepts.views import concept_delete, concept_detail, concept_edit
from clickgestion.core.utilities import custom_permission_required
from clickgestion.refunds import views
from django.conf.urls import url

urlpatterns = [

    #url(r'^$',
    #    custom_permission_required('refunds.add_refund')(views.RefundList.as_view()),
    #    name='refund_list'),

    url(r'^(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/$',
        custom_permission_required('refunds.add_refund')(concept_detail),
        {'concept_form': RefundForm},
        name='refund_detail'),
    url(r'^(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/delete/$',
        custom_permission_required('refunds.add_refund')(concept_delete),
        {'concept_form': RefundForm},
        name='refund_delete'),
    url(r'^(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/edit/$',
        custom_permission_required('refunds.add_refund')(concept_edit),
        {'concept_form': RefundForm},
        name='refund_edit'),
    url(r'^new/(?P<concept_code>T[A-F0-9]{10}-[A-Z0-9]+)/$',
        custom_permission_required('refunds.add_refund')(views.refund_new),
        name='refund_new'),
    url(r'^new/(?P<transaction_code>T[A-F0-9]{10})/$',
        custom_permission_required('refunds.add_refund')(views.refund_new),
        name='refund_new'),
]
