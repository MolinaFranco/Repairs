from django.contrib import admin
from .models import *
from django.contrib.auth.models import User, Group


class UserInline(admin.TabularInline):
    model = User
    extra = 0
class PerfilAdmin(admin.ModelAdmin):
    inlines = [UserInline]



#admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(Bitacora)
admin.site.register(Perfil)
admin.site.register(SucursalOParticular)
admin.site.register(Reparacion)
admin.site.register(Producto)
admin.site.register(Empresa)