from django.contrib import admin
from clickgestion.ticket_sales import models


class TicketSaleAdmin(admin.ModelAdmin):
    list_filter = ('start_date', 'show__name')


admin.site.register(models.Show)
admin.site.register(models.TicketSale, TicketSaleAdmin)
admin.site.register(models.TicketSaleSettings)
