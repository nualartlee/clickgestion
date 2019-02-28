from django.contrib import admin
from clickgestion.cash_desk.models import CashClose
from clickgestion.cash_desk.models import CashFloatDeposit, CashFloatDepositSettings
from clickgestion.cash_desk.models import CashFloatWithdrawal, CashFloatWithdrawalSettings


class CashCloseAdmin(admin.ModelAdmin):
    list_filter = ('employee',)


admin.site.register(CashClose, CashCloseAdmin)
admin.site.register(CashFloatDeposit)
admin.site.register(CashFloatDepositSettings)
admin.site.register(CashFloatWithdrawal)
admin.site.register(CashFloatWithdrawalSettings)

