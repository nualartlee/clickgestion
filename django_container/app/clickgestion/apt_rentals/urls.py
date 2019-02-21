from django.conf.urls import url
from clickgestion.apt_rentals import views

urlpatterns = [
    url(r'^new/(?P<transaction_code>T[A-F0-9]+)$', views.rental_new,
        name='rental_new'),
    url(r'^(?P<rental_id>[0-9]+)$', views.rental_detail,
        name='rental_detail'),
    url(r'^(?P<rental_id>[0-9]+)/edit/$', views.rental_edit,
        name='rental_edit'),
    url(r'^(?P<rental_id>[0-9]+)/delete/$', views.rental_delete,
        name='rental_delete'),

    url(r'^deposits/new/(?P<transaction_code>T[A-F0-9]+)$', views.deposit_new,
        name='deposit_new'),
    url(r'^deposits/(?P<deposit_id>[0-9]+)$', views.deposit_detail,
        name='deposit_detail'),
    url(r'^deposits/(?P<deposit_id>[0-9]+)/edit/$', views.deposit_edit,
        name='rental_edit'),
    url(r'^deposits/(?P<deposit_id>[0-9]+)/delete/$', views.deposit_delete,
        name='rental_delete'),
]
