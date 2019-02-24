from django.contrib import admin
from clickgestion.apt_rentals import models


class AptRentalAdmin(admin.ModelAdmin):
    list_filter = ('checkin', 'checkout')


admin.site.register(models.AptRental, AptRentalAdmin)
admin.site.register(models.AptRentalDeposit)
admin.site.register(models.AptRentalDepositSettings)
admin.site.register(models.NightRateRange)
admin.site.register(models.AptRentalSettings)
