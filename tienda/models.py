from django.conf import settings
from django.db import models
from django.utils import timezone


# Create your models here.
class Marca(models.Model):
    nombre = models.CharField(max_length=200, unique='true')

    def __str__(self):
        return self.nombre



class Producto(models.Model):
    modelo = models.CharField(max_length=200)
    nombre = models.CharField(max_length=200)
    marca = models.ForeignKey(Marca, models.PROTECT)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    unidades = models.PositiveIntegerField()
    detalles = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return '{} {}'.format(self.nombre, self.marca)
    def delete(self, using=None, keep_parents=False):
        super().delete()



class Compra(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    unidades = models.PositiveIntegerField()
    importe = models.DecimalField(max_digits=12, decimal_places=2)
    producto = models.ForeignKey(Producto, models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return '{} {}'.format(self.fecha, self.unidades)
