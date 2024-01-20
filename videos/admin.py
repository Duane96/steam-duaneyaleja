from django.contrib import admin
from .models import Base, Extra, ClaseVistaSensual, ClaseVistaSocial

# Register your models here.
admin.site.register(Base)
admin.site.register(Extra)
admin.site.register(ClaseVistaSensual)
admin.site.register(ClaseVistaSocial)