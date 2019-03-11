from django.conf.urls import url
from clickgestion.deposit_returns import views

urlpatterns = [
    url(r'^today$', views.today, name='deposit_returns_today'),
]
