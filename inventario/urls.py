from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Registrar el ViewSet
router = DefaultRouter()
router.register(r'productos', views.ProductoViewSet, basename='producto')

urlpatterns = [
    path('', views.home, name='home'),
    path('api/', include(router.urls)),
]
