import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .models import Compra
from django.db.models import Sum, Count
from .forms import *
from django.contrib import  messages

# Create your views here.
def welcome(request):
    return render(request, 'tienda/index.html', {})
@staff_member_required
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
    return render(request, 'tienda/CRUDS/edicion.html', {'formulario': formulario})

@staff_member_required
def nuevo(request):
    formulario = ProductoForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('listado')
    return render(request, 'tienda/CRUDS/crear.html', {'formulario': formulario})

@staff_member_required
def eliminar(request, id):
    producto = Producto.objects.get(id=id)
    producto.delete()
    return redirect('listado')

def comprador(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/compras/compra.html', {'productos': productos})

@transaction.atomic
@login_required
def realizar_compra(request, id):
    """Vista para calcular el recuento de la compra del stock con las unidades que compra el cliente"""
    producto = get_object_or_404(Producto, id=id)
    formulario = CompraForm(request.POST)

    if request.method=='POST':
        if formulario.is_valid():
            unidades= formulario.cleaned_data['unidades']
            #Comprobacion de que haya stock y guardado de compra#
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
            else: # Control de errores en el caso de que se pase #
                raise ValidationError('No hay suficientes unidades')
            return redirect('comprador')
    return render(request, 'tienda/compras/compra_producto.html', {'formulario': formulario})
@staff_member_required
def listado_informe(request):
    """Vista de listado de informe"""
    return render(request, 'tienda/informes/informes.html', {})

def informes_productos_marca(request):
    """Vista de listado de por marca"""
    marca = request.GET.get('marca')
    # Si la marca existe creamos un formulario propio nuestro de Marca y devolvemos el formulario y los productos cuya#
    #marca coincida#
    if marca:
        formulario = MarcaForm(request.GET)
        productos = Producto.objects.all().filter(marca=marca)
        contexto = {'productos':productos, 'formulario':formulario}
    else: #Formulario vacio#
        formulario = MarcaForm()
        contexto = {'formulario': formulario}
    return render(request, 'tienda/informes/productos_marca.html', contexto)

def informes_productos_usuario(request):
    """Vista de listado de productos por usuario"""
    username = request.GET.get('user') #Capturamos al usuario#
    if username: #Si el usuario existe muestra nuestro formulario persona para buscar por persona aquellas compras
        #realizadas por ese usuario#
        formulario = PersonaForm(request.GET)
        compras = Compra.objects.all().filter(user=username)
        contexto = {'compras':compras, 'formulario':formulario}
    else:
        formulario = PersonaForm()
        contexto = {'formulario': formulario}
    return render(request, 'tienda/informes/compras_usuario.html', contexto)

def informes_topten_vendidos(request):
    """Vista de listado de productos mas vendido por unidades"""
    productos = Producto.objects.all() #Consulta para sacar los productos mas vendidos haciendo un recuento de las unidades de un producto en concreto
    unidadesvendidas = Compra.objects.values('producto').annotate(importe_total=Sum('importe'),unidades_vendidas=Sum('unidades')).order_by('-unidades_vendidas')[:10]

    return render(request, 'tienda/informes/productos_topten_vendidos.html', {'productos':productos,'unidadesvendidas':unidadesvendidas})

def informes_topten_clientes(request):
    """Vista de listado de clientes que mas se han gastado en la tienda"""
    clientes = User.objects.all() #Consulta para sacar los cliente que mas han gastado haciendo un recuento del importe que se ha gastado un usuario en concreto
    reccompras= Compra.objects.values('user').annotate(sum_compras=Sum('importe')).order_by('-sum_compras')[:10]
    return render(request, 'tienda/informes/topten_mejores_clientes.html', {'clientes':clientes, "recompras":reccompras})

def crear_usuario(request):
    """Vista para registrar un usuario"""
    if request.method == "POST": #Nos traemos
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.add_message(request, messages.INFO, "Registrado")
            return redirect('welcome')
    form = UserCreationForm()
    return render(request, "tienda/control_usuarios/registro.html", {"register_form":form})

def iniciar_sesion(request):
    """Vista para iniciar sesion"""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect("welcome")
            else:
                return render(request, "tienda/control_usuarios/iniciar_sesion.html", {"login_form":form})
        else:
            return render(request, "tienda/control_usuarios/iniciar_sesion.html", {"login_form":form})
    form = AuthenticationForm()
    return render(request, "tienda/control_usuarios/iniciar_sesion.html", {"login_form":form})
