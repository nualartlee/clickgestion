from django.contrib import admin
from clickgestion.deposits.models import AptRentalDeposit, AptRentalDepositSettings, DepositReturn


admin.site.register(AptRentalDeposit)
admin.site.register(AptRentalDepositSettings)
admin.site.register(DepositReturn)

