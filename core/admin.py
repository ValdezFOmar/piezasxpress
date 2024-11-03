from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Car)
admin.site.register(models.CarPart)
admin.site.register(models.Part)
