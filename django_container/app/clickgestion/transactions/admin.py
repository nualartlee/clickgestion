from django.contrib import admin
from clickgestion.transactions.models import CashClose, Currency, ConceptValue, Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_filter = ('employee',)


admin.site.register(CashClose)
admin.site.register(Currency)
admin.site.register(ConceptValue)
admin.site.register(Transaction, TransactionAdmin)

