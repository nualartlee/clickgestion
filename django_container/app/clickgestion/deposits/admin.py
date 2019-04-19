from django.contrib import admin
from clickgestion.deposits import models


admin.site.register(models.AptRentalDeposit)
admin.site.register(models.AptRentalDepositSettings)
admin.site.register(models.DepositReturn)
admin.site.register(models.DepositReturnSettings)
admin.site.register(models.ParkingRentalDeposit)
admin.site.register(models.ParkingRentalDepositSettings)
admin.site.register(models.SafeRentalDeposit)
admin.site.register(models.SafeRentalDepositSettings)

