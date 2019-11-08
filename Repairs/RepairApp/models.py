from django.db import models
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Group
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    cuit = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class SucursalOParticular(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    empresa = models.ForeignKey(Empresa, on_delete = models.CASCADE, null = True, blank = True)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre

class Producto(models.Model):

    ESTADOS = (
            ('1', 'Ingresado'),
            ('2', 'Diagnosticando'),
            ('3', 'Esperando aprobacion'),
            ('4', 'Aprobado'),
            ('5', 'No aprobado'),
            ('6', 'Esperando repuestos'),
            ('7', 'Reparando'),
            ('8', 'Lista'),
            ('9', 'Entregada'),
            ('10', 'Entregada sin reparar'),
    )

    sucursal_o_particular = models.ForeignKey(SucursalOParticular,on_delete = models.CASCADE, verbose_name = 'Sucursal o Particular')
    nombre = models.CharField(max_length=30)
    modelo = models.CharField(max_length=30,null=True,blank=True)
    diagnostico = models.TextField()
    presupuesto_detallado = models.TextField(verbose_name='Presupuesto detallado', null = True)
    estado = models.CharField(max_length=1, choices=ESTADOS)

    def __str__(self):
        return self.nombre

class Reparacion(models.Model):
    fecha_ingreso = models.DateField(auto_now = True)
    fecha_estimada = models.DateField(null = True)
    descripcion_reparacion = models.TextField()
    producto = models.ForeignKey(Producto, on_delete = models.CASCADE)

class Bitacora(models.Model):
    fecha = models.DateField()
    titulo = models.CharField(max_length = 100, verbose_name='Título')
    descripcion_trabajo = models.TextField(verbose_name='Descripción del trabajo')
    reparacion = models.ForeignKey(Reparacion, on_delete= models.CASCADE)

    def __str__(self):
        return self.titulo


class MyUserManager(BaseUserManager):
    def create_user(self, email, nivel, password = None):
        if not email:
            raise ValueError('Los usuarios deben tener una un mail')
        user_obj = self.model(
            email = self.normalize_email(email)
            )
        user_obj.set_password(password)
        if nivel == '2' or nivel == '3':
            grupo = Group.objects.get(name='Vidente') 
            grupo.user_set.add(user_obj)
        elif nivel == '1':
            grupo = Group.objects.get(name= 'Técnico')
            grupo.user_set.add(user_obj)
        user_obj.is_staff = True
        user_obj.is_active = True
        user_obj.save(using=self.db)
        return user_obj
    def create_superuser(self, email, password = None):
        user_obj = self.model(
            email = self.normalize_email(email))
        user_obj.set_password(password)
        user_obj.is_superuser = True
        user_obj.save(using=self.db)
        return user_obj


class MyUser(AbstractBaseUser, PermissionsMixin):
    objects = MyUserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    #NIVELES = [
     #   ('1', 'Técnico'),
      #  ('2', 'Dueño'),
       # ('3', 'Empleado de Sucursal')]

    sucursal_o_particular = models.ForeignKey(SucursalOParticular, on_delete = models.CASCADE, null = True, blank = True)
    #nivel = models.CharField(max_length=1, choices=NIVELES, null = True)

    email = models.EmailField(_('email address'), blank=False, unique = True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=True,
        help_text=_('Puede loggearse en esta página.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Quitar este parámetro en lugar de borrar cuentas'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = MyUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        return self.email

    def get_short_name(self):
        """Return the short name for the user."""
        return self.email

