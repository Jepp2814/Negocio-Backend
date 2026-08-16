from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"productos", views.ProductoViewSet, basename="producto")

urlpatterns = [path("", views.home, name="home"),
               path("health/", views.health_check, name="health_check"),
               path("registro/", views.registro, name="registro"),
               path("registro-exitoso/", views.registro_exitoso, name="registro_exitoso"),
               path("login-perfil/<int:user_id>/", views.LoginPerfilView.as_view(), name="login_perfil", ),
               path("usuarios/", views.lista_usuarios, name="lista_usuarios"),
               path("usuarios/eliminar/<int:user_id>/", views.eliminar_usuario, name="eliminar_usuario", ),
               path("api/", include(router.urls)),
               path("logout-beacon/", views.logout_beacon, name="logout_beacon"),
               path("cambiar-usuario/", views.cambiar_usuario, name="cambiar_usuario"),
               path("seleccionar-usuarios/",views.seleccionar_usuarios,name="seleccionar_usuarios",),
               path("dashboard/", views.dashboard, name="dashboard"),
               path("ventas/nueva/", views.venta_nueva, name="venta_nueva"),
               path("productos/", views.productos_menu, name="productos_menu"),
               path("productos/ingresar/", views.ingresar_producto, name="ingresar_producto",
               ),
]