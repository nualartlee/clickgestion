from django.conf.urls import url
from clickgestion.transactions import views

urlpatterns = [
    url(r'^$', views.ConceptList.as_view(), name='concept_list'),
]
