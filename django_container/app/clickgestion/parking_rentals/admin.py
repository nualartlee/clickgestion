from django.contrib import admin
from clickgestion.parking_rentals import models


class ParkingRentalAdmin(admin.ModelAdmin):
    list_filter = ('start_date', 'end_date')


admin.site.register(models.ParkingRental, ParkingRentalAdmin)
admin.site.register(models.ParkingRentalSettings)
