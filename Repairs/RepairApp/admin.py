from django.contrib import admin
from RepairApp.models import *

# Register your models here.

class SucursalInline(admin.TabularInline):
    model = Sucursal
    extra = 0

class BitacoraInline(admin.TabularInline):
    model = Bitacora
    extra = 0

admin.site.register(Bitacora)

admin.site.register(Producto)

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    inlines = [SucursalInline, ]

admin.site.register(Persona)

admin.site.register(Sucursal)

@admin.register(Reparaciones)
class ReparacionesAdmin(admin.ModelAdmin):
    inlines = [BitacoraInline, ]

admin.site.register(Empleado)

admin.site.register(Particular)
