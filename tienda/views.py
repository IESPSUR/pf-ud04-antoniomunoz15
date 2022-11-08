from django.shortcuts import render
from .models import Producto
from .forms import F_prod

# Create your views here.
def welcome(request):
    return render(request,'tienda/index.html', {})

def g_productos(request):
    productos = F_prod()
    return render(request,'tienda/g_productos.html', {'form':productos})

def procesar_formulario(request):
   listado = Producto.objects.all()
   productos = F_prod()
   if productos.is_valid():
       productos.save()
       productos = F_prod()

   return render(request,'tienda/g_productos.html)',{"listado":listado,'form':productos, "mensaje": 'OK'})