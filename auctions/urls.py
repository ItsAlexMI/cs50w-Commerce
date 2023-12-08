from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("crearlistado", views.crearlistado, name="crearlistado"),
    path('mostrar_detalle/<int:listado_id>/', views.mostrar_detalle_listado, name='mostrar_detalle'),
    path('seguir_listado/<int:listado_id>/', views.seguir_listado, name='seguir_listado'),
    path('dejar_seguir_listado/<int:listado_id>/', views.dejar_seguir_listado, name='dejar_seguir_listado'),
    path('crearcomentario/<int:listado_id>/', views.crearcomentario, name='crearcomentario'),
    path('haceroferta/<int:listado_id>/', views.haceroferta, name='haceroferta'),
    path('mislistados', views.MiListaSeguimiento, name='mislistados'),
    path('cerrar_subasta/<int:listado_id>/', views.cerrar_subasta, name='cerrar_subasta'),
    path('mostrar_detalle/<int:listado_id>/', views.mostrar_detalle_listado, name='mostrar_detalle_listado'),

]
