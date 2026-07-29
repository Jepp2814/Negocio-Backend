from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CuentaViewSet,
    CategoriaFinancieraViewSet,
    MovimientoFinancieroViewSet,
    resumen_financiero,
)

router = DefaultRouter()
router.register(r'accounts', CuentaViewSet, basename='finance-accounts')
router.register(r'categories', CategoriaFinancieraViewSet, basename='finance-categories')
router.register(r'transactions', MovimientoFinancieroViewSet, basename='finance-transactions')

urlpatterns = [
    path('', include(router.urls)),
    path('summary/', resumen_financiero, name='finance-summary'),
]

