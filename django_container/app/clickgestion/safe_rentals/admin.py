from django.contrib import admin
from clickgestion.safe_rentals import models


class SafeRentalAdmin(admin.ModelAdmin):
    list_filter = ('start_date', 'end_date')


admin.site.register(models.SafeRental, SafeRentalAdmin)
admin.site.register(models.SafeRentalSettings)
