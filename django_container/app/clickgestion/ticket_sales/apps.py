from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class TicketSalesConfig(AppConfig):
    name = 'clickgestion.ticket_sales'
    verbose_name = gettext_lazy('Ticket Sales')

