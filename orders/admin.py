from django.contrib import admin

from . import models

admin.site.register(models.Quotation)
admin.site.register(models.QuotationPart)
