from django.contrib import admin
from clickgestion.transactions.models import Transaction, Concept


class TransactionAdmin(admin.ModelAdmin):
    list_filter = ('employee',)


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Concept)

