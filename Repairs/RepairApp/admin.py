from django.contrib import admin
from .models import *
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.contrib import admin, messages
from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.admin.utils import unquote
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import (
    AdminPasswordChangeForm, UserChangeForm, UserCreationForm,
)
from django.contrib.auth.models import Group, User
from django.core.exceptions import PermissionDenied
from django.db import router, transaction
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.utils.translation import gettext, gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
import json
from django.contrib.auth.forms import *
from django.contrib.auth.models import Permission
from django.shortcuts import redirect
from RepairApp.utils import renderizar_pdf

csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())

admin.site.site_header = _("Repairs Administration")
admin.site.site_title = _("My Repairs Admin")
class MyUserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)


    class Meta:
        model = MyUser
        fields = ()

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(MyUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


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
    search_fields = ('sucursal_o_particular__nombre', 'nombre', 'modelo')
    list_filter = ('estado','nombre')
    inlines = [ReparacionInline]

    def get_list_display(self, request):
        if request.user.is_superuser or request.user.nivel == '1':
            return ('sucursal_o_particular', 'nombre', 'modelo', 'estado')
        else:
            return ('nombre', 'modelo', 'estado')

    def get_fields(self, request, obj = None):
        if obj:
            if request.user.is_superuser or request.user.nivel == '1':
                return ('sucursal_o_particular','nombre','modelo','estado', 'presupuesto_detallado','diagnostico')
            elif request.user.nivel == '2':
                return ('nombre', 'modelo','estado','presupuesto_detallado', 'diagnostico')
            else:
                return('nombre', 'modelo', 'estado')
        else:
            return ('sucursal_o_particular','nombre','modelo','estado', 'presupuesto_detallado','diagnostico')

    def get_queryset(self, request):
        qs = super(ProductoAdmin, self).get_queryset(request)
        if request.user.is_superuser or request.user.nivel == '1':
            return qs

        return qs.filter(sucursal_o_particular = request.user.sucursal_o_particular)
    actions = ['generar_reporte']

    def generar_reporte(self, request, queryset):
        return renderizar_pdf('detail.html', queryset)

class ReparacionAdmin(admin.ModelAdmin):
    list_display = ('fecha_ingreso', 'fecha_estimada', 'descripcion_reparacion', 'producto')
    inlines = [BitacoraInline]
    change_list_template = 'graficos.html'

    def changelist_view(self, request, extra_context=None):

        chart_data = (
            Reparacion.objects.annotate(date=TruncDay("fecha_estimada"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )

        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        return super().changelist_view(request, extra_context=extra_context)

class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cuit')
    inlines = [SucursalOParticularInline]

class BitacoraAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'titulo', 'descripcion_trabajo', 'reparacion')

class MyUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'sucursal_o_particular', 'active', 'admin')
class MoUserAdmin(admin.ModelAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('email', 'password','sucursal_o_particular')}),
        (_('Permissions'), {
            'fields': ('is_active','nivel',),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'nivel', 'sucursal_o_particular'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['nivel','sucursal_o_particular']
        else:
            return []

    form = UserChangeForm
    add_form = MyUserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('email', 'is_staff')
    list_filter = ('is_active',)
    search_fields = ('email',)
    ordering = ('email',)



    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def get_urls(self):
        return [
            path(
                '<id>/password/',
                self.admin_site.admin_view(self.user_change_password),
                name='auth_user_password_change',
            ),
        ] + super().get_urls()

    def lookup_allowed(self, lookup, value):
        # Don't allow lookups involving passwords.
        return not lookup.startswith('password') and super().lookup_allowed(lookup, value)

    @sensitive_post_parameters_m
    @csrf_protect_m
    def add_view(self, request, form_url='', extra_context=None):
        with transaction.atomic(using=router.db_for_write(self.model)):
            return self._add_view(request, form_url, extra_context)

    def _add_view(self, request, form_url='', extra_context=None):
        # It's an error for a user to have add permission but NOT change
        # permission for users. If we allowed such users to add users, they
        # could create superusers, which would mean they would essentially have
        # the permission to change users. To avoid the problem entirely, we
        # disallow users from adding users if they don't have change
        # permission.
        if not self.has_change_permission(request):
            if self.has_add_permission(request) and settings.DEBUG:
                # Raise Http404 in debug mode so that the user gets a helpful
                # error message.
                raise Http404(
                    'Your user does not have the "Change user" permission. In '
                    'order to add users, Django requires that your user '
                    'account have both the "Add user" and "Change user" '
                    'permissions set.')
            raise PermissionDenied
        if extra_context is None:
            extra_context = {}
        username_field = self.model._meta.get_field(self.model.USERNAME_FIELD)
        defaults = {
            'auto_populated_fields': (),
            'username_help_text': username_field.help_text,
        }
        extra_context.update(defaults)
        return super().add_view(request, form_url, extra_context)

    @sensitive_post_parameters_m
    def user_change_password(self, request, id, form_url=''):
        user = self.get_object(request, unquote(id))
        if not self.has_change_permission(request, user):
            raise PermissionDenied
        if user is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {
                'name': self.model._meta.verbose_name,
                'key': escape(id),
            })
        if request.method == 'POST':
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                change_message = self.construct_change_message(request, form, None)
                self.log_change(request, user, change_message)
                msg = gettext('Password changed successfully.')
                messages.success(request, msg)
                update_session_auth_hash(request, form.user)
                return HttpResponseRedirect(
                    reverse(
                        '%s:%s_%s_change' % (
                            self.admin_site.name,
                            user._meta.app_label,
                            user._meta.model_name,
                        ),
                        args=(user.pk,),
                    )
                )
        else:
            form = self.change_password_form(user)

        fieldsets = [(None, {'fields': list(form.base_fields)})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        context = {
            'title': _('Change password: %s') % escape(user.get_username()),
            'adminForm': adminForm,
            'form_url': form_url,
            'form': form,
            'is_popup': (IS_POPUP_VAR in request.POST or
                         IS_POPUP_VAR in request.GET),
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
            **self.admin_site.each_context(request),
        }

        request.current_app = self.admin_site.name

        return TemplateResponse(
            request,
            self.change_user_password_template or
            'admin/auth/user/change_password.html',
            context,
        )

    def response_add(self, request, obj, post_url_continue=None):
        """
        Determine the HttpResponse for the add_view stage. It mostly defers to
        its superclass implementation but is customized because the User model
        has a slightly different workflow.
        """
        # We should allow further modification of the user just added i.e. the
        # 'Save' button should behave like the 'Save and continue editing'
        # button except in two scenarios:
        # * The user has pressed the 'Save and add another' button
        # * We are adding a user in a popup
        if '_addanother' not in request.POST and IS_POPUP_VAR not in request.POST:
            request.POST = request.POST.copy()
            request.POST['_continue'] = 1
        return super().response_add(request, obj, post_url_continue)



admin.site.unregister(Group)
admin.site.register(MyUser, MoUserAdmin)
admin.site.register(Bitacora,BitacoraAdmin)
admin.site.unregister(Bitacora)
admin.site.register(SucursalOParticular,SucursalOParticularAdmin)
admin.site.register(Reparacion,ReparacionAdmin)
admin.site.register(Producto,ProductoAdmin)
admin.site.register(Empresa,EmpresaAdmin)
