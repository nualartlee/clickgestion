from django.conf.urls import url
from clickgestion.transactions import views

urlpatterns = [
    url(r'^$', views.ConceptList.as_view(), name='concept_list'),
    url(r'^(?P<concept_code>T[-A-Z0-9]+)/$', views.concept_row,
        name='concept_row'),
]
