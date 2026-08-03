from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Producto
from .serializers import ProductoSerializer

# Vista home simple
def home(request):
    return JsonResponse({
        "message": "Sitio funcionando ✅",
        "api": "/api/productos/",
        "health": "/health/"
    })


def health_check(request):
    return JsonResponse({"status": "ok", "app": "negocio-backend"})

# ViewSet REST API para Productos
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['codigo', 'nombre']
    ordering_fields = ['created_at', 'precio_venta', 'stock']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def bajo_stock(self, request):
        """Retorna productos con stock bajo (< 5 unidades)"""
        umbral = int(request.query_params.get('umbral', 5))
        productos = self.queryset.filter(stock__lt=umbral)
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def aumentar_stock(self, request):
        """Aumenta el stock de un producto"""
        producto = self.get_object()
        cantidad = request.data.get('cantidad', 0)
        try:
            cantidad = int(cantidad)
            if cantidad < 0:
                return Response(
                    {'error': 'La cantidad debe ser positiva'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            producto.stock += cantidad
            producto.save()
            serializer = self.get_serializer(producto)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                {'error': 'Cantidad inválida'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def disminuir_stock(self, request):
        """Disminuye el stock de un producto"""
        producto = self.get_object()
        cantidad = request.data.get('cantidad', 0)
        try:
            cantidad = int(cantidad)
            if cantidad < 0:
                return Response(
                    {'error': 'La cantidad debe ser positiva'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if producto.stock < cantidad:
                return Response(
                    {'error': 'Stock insuficiente'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            producto.stock -= cantidad
            producto.save()
            serializer = self.get_serializer(producto)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                {'error': 'Cantidad inválida'},
                status=status.HTTP_400_BAD_REQUEST
            )

# Vista Temporal del Dashboard
from django.shortcuts import render

def dashboard(request):
    return render(request, "dashboard/dashboard.html")