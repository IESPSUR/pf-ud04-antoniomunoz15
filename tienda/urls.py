from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('tienda/', views.welcome, name='welcome'),
    path('tienda/admin/listado', views.listado, name='listado'),
    path('tienda/admin/edicion', views.edicion, name='edicion'),
    path('tienda/admin/edicion/<int:id>', views.edicion, name='edicion'),
    path('tienda/admin/nuevo', views.nuevo, name='nuevo'),
    path('tienda/admin/eliminar/<int:id>', views.eliminar, name='eliminar'),
    path('tienda/listadocompra/', views.comprador, name='comprador'),
    path('tienda/realizar_compra/<int:id>', views.realizar_compra, name='realizar_compra'),
    path('tienda/informes/', views.listado_informe, name='listado_informes'),
    path('tienda/informes/productosPorMarca', views.informes_productos_marca, name='listado_marca'),
    path('tienda/informes/compras_usuario', views.informes_productos_usuario, name='compra_usuario'),
    path('tienda/informes/productos_topten', views.informes_topten_vendidos, name='informe_topten_producto'),
    path('tienda/informes/top_clientes', views.informes_topten_clientes, name='informe_topten_clientes'),
    path('tienda/registro', views.crear_usuario, name='registro'),
    path('tienda/login', views.iniciar_sesion, name='iniciosesion'),
]
