from django.shortcuts import render
from .models import Producto

# Create your views here.
def welcome(request):
    return render(request,'tienda/index.html', {})

def g_productos(request):
    productos = Producto.objects.all()
    return render(request,'tienda/g_productos.html', {'productos':productos})
