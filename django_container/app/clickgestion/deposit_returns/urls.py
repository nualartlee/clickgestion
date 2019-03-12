from django.conf.urls import url
from clickgestion.deposit_returns import views

urlpatterns = [
    url(r'^(?P<concept_code>T[-A-Z0-9]+)/$', views.deposit_return,
        name='deposit_return'),
    url(r'^today$', views.today, name='deposit_returns_today'),
]
