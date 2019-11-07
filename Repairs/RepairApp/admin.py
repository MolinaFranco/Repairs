from django.contrib import admin
from .models import *
from django.contrib.auth.models import User, Group

class ProductoInline(admin.TabularInline):
    model = Producto
    extra = 0

class SucursalOParticularAdmin (admin.ModelAdmin):
    inlines = [ProductoInline]
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['sucursal_o_particular']
    
    #def get_queryset(self, request):
     #   qs = super(ProductoAdmin, self).get_queryset(request)
      #  if request.user.is_superuser or User.objects.filter(pk=request.user.id, groups__name='Técnico').exists():
       #     return qs

        #return qs.filter(sucursal_o_particular = request.user.perfil.id)

            
        
        

#admin.site.unregister(User)
#admin.site.unregister(Group)
admin.site.register(MyUser)
admin.site.register(Bitacora)
admin.site.register(SucursalOParticular,SucursalOParticularAdmin)
admin.site.register(Reparacion)
admin.site.register(Producto,ProductoAdmin)
admin.site.register(Empresa)