from django.conf.urls import url
from clickgestion.transactions import views

urlpatterns = [
    url(r'^new/$', views.new_transaction, name='newtransaction'),
]
