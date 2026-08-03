from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Producto
from .serializers import ProductoSerializer
from .forms import RegistroUsuarioForm


def home(request):
    return JsonResponse({
        "message": "Sitio funcionando ✅",
        "api": "/api/productos/",
        "health": "/health/"
    })


def health_check(request):
    return JsonResponse({"status": "ok", "app": "negocio-backend"})


def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            messages.success(request, 'Su usuario fue creado correctamente.')
            return redirect('registro_exitoso')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'registration/register.html', {'form': form})


def registro_exitoso(request):
    return render(request, 'registration/register_success.html')

@csrf_exempt
@require_POST
def logout_beacon(request):
    if request.user.is_authenticated:
        logout(request)
    return JsonResponse({'ok': True})

@staff_member_required
def lista_usuarios(request):
    usuarios = User.objects.all().order_by('id')
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})


@staff_member_required
@require_POST
def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)

    if usuario.username == 'Jepp':
        messages.error(request, 'No se puede eliminar el usuario Jepp.')
        return redirect('lista_usuarios')

    usuario.delete()
    messages.success(request, 'Usuario eliminado correctamente.')
    return redirect('lista_usuarios')


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['codigo', 'nombre']
    ordering_fields = ['created_at', 'precio_venta', 'stock']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def bajo_stock(self, request):
        umbral = int(request.query_params.get('umbral', 5))
        productos = self.queryset.filter(stock__lt=umbral)
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def aumentar_stock(self, request):
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