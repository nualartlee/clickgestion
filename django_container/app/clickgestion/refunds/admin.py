from django.contrib import admin
from clickgestion.refunds import models


admin.site.register(models.Refund)
admin.site.register(models.RefundSettings)

