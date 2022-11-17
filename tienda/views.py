import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .models import Compra
from django.db.models import Sum, Count
from .forms import *

# Create your views here.
def welcome(request):
    return render(request, 'tienda/index.html', {})
def listado(request):
    productos= Producto.objects.all()
    return render(request, 'tienda/listado.html', {'productos': productos})
@staff_member_required
def edicion(request, id):
    producto= Producto.objects.get(id=id)
    formulario = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('listado')
    return render(request, 'tienda/edicion.html', {'formulario': formulario})

@staff_member_required
def nuevo(request):
    formulario = ProductoForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('listado')
    return render(request, 'tienda/crear.html', {'formulario': formulario})

@staff_member_required
def eliminar(request, id):
    producto = Producto.objects.get(id=id)
    producto.delete()
    return redirect('listado')

def comprador(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/compra.html', {'productos': productos})

@transaction.atomic
@login_required
def realizar_compra(request, id):

    producto = get_object_or_404(Producto, id=id)
    formulario = CompraForm(request.POST)

    if request.method=='POST':
        if formulario.is_valid():
            unidades= formulario.cleaned_data['unidades']
            total = producto.precio * int(unidades)

            if(producto.unidades > unidades):
                producto.unidades = producto.unidades - unidades
                producto.save()

                compra = Compra()
                compra.producto = producto
                compra.unidades = unidades
                compra.user= request.user
                compra.fecha= datetime.datetime.now()
                compra.importe=unidades * producto.precio
                compra.save()

                return redirect('comprador')
    return render(request, 'tienda/compra_producto.html', {'formulario': formulario})
def listado_informe(request):
    return render(request, 'tienda/informes.html', {})

def informes_productos_marca(request):
    marca = request.GET.get('marca')
    if marca:
        formulario = MarcaForm(request.GET)
        productos = Producto.objects.all().filter(marca=marca)
        contexto = {'productos':productos, 'formulario':formulario}
    else:
        formulario = MarcaForm()
        contexto = {'formulario': formulario}
    return render(request, 'tienda/productos_marca.html', contexto)

def informes_productos_usuario(request):
    username = request.GET.get('user')
    if username:
        formulario = PersonaForm(request.GET)
        compras = Compra.objects.all().filter(user=request.user)
        contexto = {'compras':compras, 'formulario':formulario}
    else:
        formulario = PersonaForm()
        contexto = {'formulario': formulario}
    return render(request, 'tienda/compras_usuario.html', contexto)

def informes_topten_vendidos(request):
    productos = Producto.objects.annotate(sum_ventas=Sum('compra__unidades'),
                                          sum_importes=Sum('compra__importe')).order_by('-sum_ventas')[:10]
    return render(request,'tienda/productos_topten_vendidos.html', {'productos':productos})

def informes_topten_clientes(request):
    clientes = User.objects.annotate(importe_compras=Sum('compra__importe'),
                                          total_compra=Count('compra')).order_by('-importe_compras')[:10]
    return render(request,'tienda/topten_mejores_clientes.html', {'clientes':clientes})