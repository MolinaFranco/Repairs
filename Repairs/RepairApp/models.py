from django.db import models
from django.contrib.auth.models import User

class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    CUIT = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class SucursalOParticular(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre Completo')
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

class Perfil(models.Model):
    class Meta:
        verbose_name_plural = 'Perfiles'
    NIVELES = [
        ('1', 'Técnico'),
        ('2', 'Dueño'),
        ('3', 'Empleado de Sucursal'),]

    usuario = models.OneToOneField(User, on_delete = models.CASCADE)
    sucursal_o_particular = models.ForeignKey(SucursalOParticular, on_delete = models.CASCADE)
    nivel = models.CharField(max_length=1, choices=NIVELES, default = '3')
    