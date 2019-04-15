from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class ServiceSalesConfig(AppConfig):
    name = 'clickgestion.service_sales'
    verbose_name = gettext_lazy('Service Sales')

