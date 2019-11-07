from django.db import models
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    CUIT = models.CharField(max_length=100)

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
            raise ValueError('Los usuarios deben tener una contraseña')
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
        user_obj.save(using=self.db)
        return user_obj


class MyUser(AbstractBaseUser):
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
    active = models.BooleanField(verbose_name = 'Está activo', default = True)# Está activo
    staff = models.BooleanField(default = True)
    admin = models.BooleanField(verbose_name = 'Es administrador', default = False)# es admin
    email = models.EmailField(verbose_name = 'E-mail', unique = True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_email(self):
        return self.email
    
    #def get_nivel(self):
     #   return self.nivel
    
    def get_username(self):
        return self.get_email()

    def get_short_name(self):
        return self.email
    
    def get_full_name(self):
        return self.email
    
    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_active(self):
        return self.active
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True

