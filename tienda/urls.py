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
    path('tienda/listadoInformes/', views.listado_informe, name='listado_informes'),
]
