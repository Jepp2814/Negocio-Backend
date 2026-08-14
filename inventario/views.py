from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.views import LoginView
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Producto
from .serializers import ProductoSerializer
from .forms import RegistroUsuarioForm, ProductoForm


User = get_user_model()


def get_perfiles_disponibles():
    return User.objects.filter(is_active=True).order_by(
        "first_name",
        "last_name",
        "username",
        "id",
    )


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    return redirect("login")


class LoginConPerfilesView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("usuarios", get_perfiles_disponibles())
        return context


class LoginPerfilView(LoginConPerfilesView):

    def get_initial(self):
        initial = super().get_initial()

        usuario = get_object_or_404(
            User,
            pk=self.kwargs["user_id"],
            is_active=True,
        )

        initial["username"] = usuario.username

        return initial


def health_check(request):
    return JsonResponse({
        "status": "ok",
        "app": "negocio-backend",
    })


def registro(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.save()

            messages.success(
                request,
                "Su usuario fue creado correctamente. Ahora puede elegir su perfil para iniciar sesión."
            )

            return redirect("login")
    else:
        form = RegistroUsuarioForm()

    return render(
        request,
        "registration/register.html",
        {"form": form},
    )


def registro_exitoso(request):
    return render(
        request,
        "registration/register_success.html",
    )


@csrf_exempt
@require_POST
def logout_beacon(request):
    if request.user.is_authenticated:
        logout(request)

    return JsonResponse({"ok": True})


@staff_member_required
def lista_usuarios(request):
    usuarios = User.objects.all().order_by("id")

    return render(
        request,
        "usuarios/lista_usuarios.html",
        {"usuarios": usuarios},
    )


@login_required
@require_POST
def cambiar_usuario(request):
    logout(request)

    return redirect("home")


@staff_member_required
@require_POST
def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)

    if usuario.username == "Jepp":
        messages.error(
            request,
            "No se puede eliminar el usuario Jepp."
        )
        return redirect("lista_usuarios")

    usuario.delete()

    messages.success(
        request,
        "Usuario eliminado correctamente."
    )

    return redirect("lista_usuarios")


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["codigo", "^nombre"]
    ordering_fields = ["fecha_creacion", "precio_venta", "stock"]
    ordering = ["-fecha_creacion"]

    @action(detail=False, methods=["get"])
    def bajo_stock(self, request):
        umbral = int(request.query_params.get("umbral", 5))

        productos = self.queryset.filter(stock__lt=umbral)

        serializer = self.get_serializer(
            productos,
            many=True,
        )

        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def aumentar_stock(self, request):
        producto = self.get_object()
        cantidad = request.data.get("cantidad", 0)

        try:
            cantidad = int(cantidad)

            if cantidad < 0:
                return Response(
                    {"error": "La cantidad debe ser positiva"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            producto.stock += cantidad
            producto.save()

            serializer = self.get_serializer(producto)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        except ValueError:
            return Response(
                {"error": "Cantidad inválida"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["post"])
    def disminuir_stock(self, request):
        producto = self.get_object()
        cantidad = request.data.get("cantidad", 0)

        try:
            cantidad = int(cantidad)

            if cantidad < 0:
                return Response(
                    {"error": "La cantidad debe ser positiva"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if producto.stock < cantidad:
                return Response(
                    {"error": "Stock insuficiente"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            producto.stock -= cantidad
            producto.save()

            serializer = self.get_serializer(producto)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        except ValueError:
            return Response(
                {"error": "Cantidad inválida"},
                status=status.HTTP_400_BAD_REQUEST,
            )


@login_required
def dashboard(request):
    return render(
        request,
        "dashboard/dashboard.html",
    )


@login_required
def venta_nueva(request):
    return render(
        request,
        "dashboard/venta_nueva.html",
    )


@login_required
def productos_menu(request):
    return render(
        request,
        "dashboard/productos.html",
    )


@login_required
def ingresar_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)

        if form.is_valid():
            producto = form.save()

            messages.success(
                request,
                (
                    "Los cambios se guardaron exitosamente. "
                    f"Producto creado: {producto.nombre}. "
                    f"Código del producto: {producto.codigo}."
                ),
                extra_tags="producto_guardado",
            )

            return redirect("ingresar_producto")
    else:
        form = ProductoForm()

    return render(
        request,
        "dashboard/ingresar_producto.html",
        {"form": form},
    )