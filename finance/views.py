from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Cuenta, CategoriaFinanciera, MovimientoFinanciero
from .serializers import (
    CuentaSerializer,
    CategoriaFinancieraSerializer,
    MovimientoFinancieroSerializer,
)

class CuentaViewSet(viewsets.ModelViewSet):
    queryset = Cuenta.objects.all()
    serializer_class = CuentaSerializer

class CategoriaFinancieraViewSet(viewsets.ModelViewSet):
    queryset = CategoriaFinanciera.objects.all()
    serializer_class = CategoriaFinancieraSerializer

class MovimientoFinancieroViewSet(viewsets.ModelViewSet):
    queryset = MovimientoFinanciero.objects.select_related('cuenta', 'categoria').all()
    serializer_class = MovimientoFinancieroSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        tipo = self.request.query_params.get('tipo')
        cuenta = self.request.query_params.get('cuenta')
        categoria = self.request.query_params.get('categoria')

        if tipo:
            queryset = queryset.filter(tipo=tipo)
        if cuenta:
            queryset = queryset.filter(cuenta_id=cuenta)
        if categoria:
            queryset = queryset.filter(categoria_id=categoria)

        return queryset
    
@api_view(['GET '])
def resumen_financiero(request):
    ingresos = MovimientoFinanciero.objects.filter(tipo='ingreso').aggregate(total=Sum('monto'))['total']or 0
    egresos = MovimientoFinanciero.objects.filter(tipo='egreso').aggregate(total=Sum('monto'))['total']or 0
    saldo_inicial = Cuenta.objects.aggregate(total=Sum('saldo_inicial'))['total']or 0
    saldo_actual = saldo_inicial + ingresos - egresos

    return Response ({
        'ingresos': ingresos,
        'egresos': egresos,
        'saldo_inicial': saldo_inicial,
        'saldo_actual': saldo_actual
    })