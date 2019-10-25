from django.db import models

# Create your models here.

class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento =  models.DateField()
    DNI = models.CharField(max_length=30)
    direccion =  models.CharField(max_length=100)
    telefono =  models.CharField(max_length=30)


class Particular(models.Model):
    pass

class Empleado(models.Model):
    pass

class Bitacora(models.Model):
    fecha = models.DateField()
    descripcion_trabajo = models.TextField()
    compras = models.TextField()
    gastos = models.PositiveIntegerField()


class Reparaciones(models.Model):
    fecha_ingreso = models.DateField()
    fecha_estimada = models.DateField()
    descripcion_reparacion = models.TextField()


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

    nombre = models.CharField(max_length=30)
    modelo = models.CharField(max_length=30,null=True,blank=True)
    diag_primera_vista =models.TextField()
    diag_profundidad =models.TextField(null=True,blank=True)
    presupuesto = models.PositiveIntegerField()
    estado = models.CharField(max_length=1, choices=ESTADOS)


class Sucursal(models.Model):
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)


class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    dueño = models.CharField(max_length=100)
    CUIT = models.CharField(max_length=100)
