from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('tienda/', views.welcome, name='welcome'),
    path('tienda/listado', views.listado, name='listado'),
    path('tienda/edicion', views.edicion, name='edicion'),
    path('tienda/edicion/<int:id>', views.edicion, name='edicion'),
    path('tienda/nuevo', views.nuevo, name='nuevo'),
    path('tienda/eliminar/<int:id>', views.eliminar, name='eliminar'),
]
