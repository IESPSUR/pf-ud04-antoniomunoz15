from django.conf import settings
from django.db import models
from django.utils import timezone


# Create your models here.
class Marca(models.Model):
    nombre = models.CharField(max_length=200, primary_key='true')



class Producto(models.Model):
    modelo = models.CharField(max_length=200)
    nombre = models.CharField(max_length=200)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    precio = models.IntegerField()
    unidades = models.IntegerField()
    detalles = models.CharField(max_length=500)

    def __str__(self):
        return '{} {}'.format(self.nombre, self.marca)
    def delete(self, using=None, keep_parents=False):
        super().delete()



class Compra(models.Model):
    fecha = models.CharField(max_length=200)
    unidades = models.CharField(max_length=200)
    importe = models.CharField(max_length=200)


