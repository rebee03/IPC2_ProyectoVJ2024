from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('carga/', views.admincarga, name='carga'),
    path('user/', views.userview, name='user'),
    path('signin/', views.signin, name='signin'),
    path('cargaxml/', views.cargarXML, name='cargaxml'),
    path('xmlproductos/', views.enviarProductos, name='xmlproductos'),
    path('xmlusuarios/', views.enviarUsuarios, name='xmlusuarios'),
    path('xmlempleados/', views.enviarEmpleados, name='xmlempleados'),
    path('xmlactividades/', views.enviarActividades, name='xmlactividades'),
    path('productos/', views.verProductos, name='productos'),
    path('estadisticas/', views.verEstadisticas, name='estadisticas'),
    path('pdf/', views.verPDF, name='pdf'),
    path('logout/', views.logout, name='logout'),

    path('comprar/', views.comprarPage, name='comprar'),

    path('search/', views.buscarProducto, name='search'),
    path('addCart/', views.agregarCarrito, name='addCart'),
    path('vercarrito/', views.verCarrito, name='vercarrito'),

    path('compro/', views.comprar, name='compro'),
# Prueba
    path('verCompras/', views.verCompras, name='verCompras'),
    path('datosEstudiantes/', views.informacionEstudiantes, name='datosEstudiantes'),
    path('actividades/', views.verActividades, name='actividades'),
]