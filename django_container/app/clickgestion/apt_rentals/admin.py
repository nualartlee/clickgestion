from django.contrib import admin
from clickgestion.apt_rentals.models import AptRental, AptRentalDeposit, NightRateRange, AptRentalSettings


class AptRentalAdmin(admin.ModelAdmin):
    list_filter = ('checkin', 'checkout')


admin.site.register(AptRental, AptRentalAdmin)
admin.site.register(AptRentalDeposit)
admin.site.register(NightRateRange)
admin.site.register(AptRentalSettings)
