from django.shortcuts import render, redirect
from .models import Producto
from .forms import ProductoForm

# Create your views here.
def welcome(request):
    return render(request, 'tienda/index.html', {})
def listado(request):
    productos= Producto.objects.all()
    return render(request, 'tienda/listado.html', {'productos': productos})
def edicion(request, id):
    producto= Producto.objects.get(id=id)
    formulario = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('listado')
    return render(request, 'tienda/edicion.html', {'formulario': formulario})
def nuevo(request):
    formulario = ProductoForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('listado')
    return render(request, 'tienda/crear.html', {'formulario': formulario})

def eliminar(request, id):
    producto = Producto.objects.get(id=id)
    producto.delete()
    return redirect('listado')

def compra(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/realizar_compra.html', {'productos': productos})

def realizar_compra(request, id):
    producto = Producto.objects.get(id=id)
    formulario = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('listado')
    return render(request, 'tienda/Detalles_Compra_Producto.html', {'formulario': formulario})
