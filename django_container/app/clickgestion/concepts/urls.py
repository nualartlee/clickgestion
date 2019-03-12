from django.conf.urls import url
from clickgestion.concepts import views

urlpatterns = [
    url(r'^$', views.ConceptList.as_view(), name='concept_list'),
    url(r'^(?P<concept_code>T[-A-Z0-9]+)/$', views.concept_row,
        name='concept_row'),
    url(r'^(?P<concept_code>T[-A-Z0-9]+)/delete/$', views.concept_delete,
        name='concept_delete'),
    url(r'^(?P<concept_code>T[-A-Z0-9]+)/detail/$', views.concept_detail,
        name='concept_detail'),
    url(r'^(?P<concept_code>T[-A-Z0-9]+)/refund/$', views.concept_refund,
        name='concept_refund'),
]
