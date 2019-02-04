from django.conf.urls import url
from clickgestion.main import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
