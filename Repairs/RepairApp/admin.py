from django.contrib import admin
from .models import *
from django.contrib.auth.models import User, Group

class ProductoInline(admin.TabularInline):
    model = Producto
    extra = 0

class BitacoraInline(admin.TabularInline):
    model = Bitacora
    extra = 0

class SucursalOParticularInline(admin.TabularInline):
    model = SucursalOParticular
    extra = 0

class ReparacionInline(admin.TabularInline):
    model = Reparacion
    extra = 0

class SucursalOParticularAdmin (admin.ModelAdmin):
    list_display = ('nombre', 'empresa', 'direccion', 'telefono')
    inlines = [ProductoInline]

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('sucursal_o_particular', 'nombre', 'modelo', 'diagnostico', 'presupuesto_detallado', 'estado')
    inlines = [ReparacionInline]

class ReparacionAdmin(admin.ModelAdmin):
    list_display = ('fecha_ingreso', 'fecha_estimada', 'descripcion_reparacion', 'producto')
    inlines = [BitacoraInline]

class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cuit')
    inlines = [SucursalOParticularInline]

class BitacoraAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'titulo', 'descripcion_trabajo', 'reparacion')

class MyUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'sucursal_o_particular', 'active', 'admin')


    
    #def get_queryset(self, request):
     #   qs = super(ProductoAdmin, self).get_queryset(request)
      #  if request.user.is_superuser or User.objects.filter(pk=request.user.id, groups__name='Técnico').exists():
       #     return qs

        #return qs.filter(sucursal_o_particular = request.user.perfil.id)

            
        
        

#admin.site.unregister(User)
#admin.site.unregister(Group)
admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Bitacora,BitacoraAdmin)
admin.site.register(SucursalOParticular,SucursalOParticularAdmin)
admin.site.register(Reparacion,ReparacionAdmin)
admin.site.register(Producto,ProductoAdmin)
admin.site.register(Empresa,EmpresaAdmin)