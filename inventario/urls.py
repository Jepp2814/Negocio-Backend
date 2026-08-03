from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'productos', views.ProductoViewSet, basename='producto')


urlpatterns = [
    path('', views.home, name='home'),
    path('health/', views.health_check, name='health_check'),
    path('registro/', views.registro, name='registro'),
    path('registro-exitoso/', views.registro_exitoso, name='registro_exitoso'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('api/', include(router.urls)),
    path('logout-beacon/', views.logout_beacon, name='logout_beacon'),
]