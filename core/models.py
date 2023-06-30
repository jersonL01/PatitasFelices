from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class TipoProducto(models.Model):
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.IntegerField()
    descripcion = models.CharField(max_length=200)
    tipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    vencimiento = models.DateField()
    imagen = models.ImageField(null=True,blank=True)
    vigente = models.BooleanField()

    def __str__(self):
        return self.nombre
        
class TipoCliente(models.Model):
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.tipo

class Cliente(models.Model):
    rut = models.CharField(max_length=12)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    telefono = models.IntegerField(max_length=100)
    direccion = models.IntegerField(max_length=100)
    contraseña= models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoCliente, on_delete=models.CASCADE)

    def __str__(self):
        return self.rut


class Cart(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    foto = models.ImageField(null=True, blank=True)
    fecha_compra = models.DateTimeField(default=timezone.now)

