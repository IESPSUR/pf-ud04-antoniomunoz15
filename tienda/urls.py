from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('tienda/', views.welcome, name='welcome'),
    path('tienda/g_productos/', views.g_productos, name='g_productos'),
    path('tienda/guardarProducto/', views.g_productos, name='guardarproducto'),
]
