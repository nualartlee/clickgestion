from django.contrib import admin
from clickgestion.service_sales import models


class ServiceSaleAdmin(admin.ModelAdmin):
    list_filter = ('start_date', 'service__name')


admin.site.register(models.ServiceType)
admin.site.register(models.Service)
admin.site.register(models.ServiceSale, ServiceSaleAdmin)
admin.site.register(models.ServiceSaleSettings)
