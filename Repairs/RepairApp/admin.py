from django.contrib import admin
from RepairApp.models import *

# Register your models here.

class SucursalInline(admin.TabularInline):
    model = Sucursal
    extra = 0

admin.site.register(Bitacora)

admin.site.register(Producto)

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    inlines = [SucursalInline, ]

admin.site.register(Persona)

admin.site.register(Sucursal)

admin.site.register(Reparaciones)

admin.site.register(Empleado)

admin.site.register(Particular)
