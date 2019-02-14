from django.contrib import admin
from clickgestion.apt_rentals.models import ApartmentRental, NightRateRange


class ApartmentRentalAdmin(admin.ModelAdmin):
    list_filter = ('checkin', 'checkout')


admin.site.register(ApartmentRental, ApartmentRentalAdmin)
admin.site.register(NightRateRange)
