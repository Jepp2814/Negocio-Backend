from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Registrar el ViewSet
router = DefaultRouter()
# python manage.py runserverrouter.register(r'productos', views.ProductoViewSet, basename='producto')

urlpatterns = [
    path('', views.home, name='home'),
    path('api/', include(router.urls)),
]