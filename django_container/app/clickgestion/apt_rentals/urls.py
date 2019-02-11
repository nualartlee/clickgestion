from django.conf.urls import url
from clickgestion.apt_rentals import views

urlpatterns = [
    url(r'^new/(?P<transaction_id>[0-9]+)$', views.rental_new,
        name='rental_new'),
]
