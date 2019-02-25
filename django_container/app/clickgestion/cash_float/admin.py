from django.contrib import admin
from clickgestion.cash_float import models

admin.site.register(models.CashFloatDeposit)
admin.site.register(models.CashFloatDepositSettings)
admin.site.register(models.CashFloatWithdrawal)
admin.site.register(models.CashFloatWithdrawalSettings)
