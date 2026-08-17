from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.views import LoginView
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models.deletion import ProtectedError

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Producto
from .serializers import ProductoSerializer
from .forms import RegistroUsuarioForm, ProductoForm, ProductoEditarForm


User = get_user_model()


def get_perfiles_disponibles():
    return User.objects.filter(is_active=True).order_by(
        "first_name",
        "last_name",
        "username",
        "id",
    )


def seleccionar_usuarios(request):
    usuarios = get_perfiles_disponibles()

    return render(
        request,
        "usuarios/seleccionar_usuario.html",
        {"usuarios": usuarios},
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
                (
                    "Su usuario fue creado correctamente. Ahora puede elegir "
                    "su perfil para iniciar sesión."
                ),
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
            "No se puede eliminar el usuario Jepp.",
        )
        return redirect("lista_usuarios")

    usuario.delete()

    messages.success(
        request,
        "Usuario eliminado correctamente.",
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


@login_required
def editar_producto(request):
    return render(
        request,
        "dashboard/editar_producto.html",
    )


@login_required
def consultar_productos(request):
    return render(
        request,
        "dashboard/consultar_productos.html",
    )


@login_required
@require_POST
def guardar_producto_editado(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)

    valores_anteriores = {
        "codigo": producto.codigo,
        "nombre": producto.nombre,
        "marca": producto.marca or "",
        "modelo": producto.modelo or "",
        "proveedor": producto.proveedor or "",
        "costo": producto.costo,
        "costo_caja": producto.costo_caja,
        "precio_venta": producto.precio_venta,
        "precio_venta_caja": producto.precio_venta_caja,
        "stock": producto.stock,
        "especificaciones": producto.especificaciones or "",
        "imagen": producto.imagen.name if producto.imagen else "",
    }

    imagen_anterior = producto.imagen if producto.imagen else None

    form = ProductoEditarForm(
        request.POST,
        request.FILES,
        producto=producto,
    )

    if form.is_valid():
        producto_actualizado = producto

        for campo in [
            "codigo",
            "nombre",
            "marca",
            "modelo",
            "proveedor",
            "costo",
            "costo_caja",
            "precio_venta",
            "precio_venta_caja",
            "stock",
            "especificaciones",
        ]:
            setattr(
                producto_actualizado,
                campo,
                form.cleaned_data[campo],
            )

        nueva_imagen = form.cleaned_data.get("imagen")

        if nueva_imagen:
            producto_actualizado.imagen = nueva_imagen

        producto_actualizado.save()

        if nueva_imagen and imagen_anterior:
            if imagen_anterior.name != producto_actualizado.imagen.name:
                imagen_anterior.delete(save=False)

        etiquetas_campos = {
            "codigo": "Código",
            "nombre": "Nombre",
            "marca": "Marca",
            "modelo": "Modelo",
            "proveedor": "Proveedor",
            "costo": "Costo por unidad",
            "costo_caja": "Costo por caja",
            "precio_venta": "Precio de venta por unidad",
            "precio_venta_caja": "Precio de venta por caja",
            "stock": "Stock",
            "especificaciones": "Especificaciones",
        }

        cambios_realizados = []

        for campo, etiqueta in etiquetas_campos.items():
            valor_anterior = valores_anteriores[campo]
            valor_nuevo = getattr(producto_actualizado, campo)

            if valor_anterior != valor_nuevo:
                cambios_realizados.append(etiqueta)

        imagen_nueva = (
            producto_actualizado.imagen.name
            if producto_actualizado.imagen
            else ""
        )

        if nueva_imagen and valores_anteriores["imagen"] != imagen_nueva:
            cambios_realizados.append("Imagen referencial")

        detalle_cambios = (
            ", ".join(cambios_realizados)
            if cambios_realizados
            else "No se modificaron campos"
        )

        messages.success(
            request,
            (
                "Los cambios se guardaron exitosamente. "
                f"Producto actualizado: {producto_actualizado.nombre}. "
                f"Código: {producto_actualizado.codigo}. "
                f"Cambios realizados: {detalle_cambios}."
            ),
            extra_tags="producto_editado",
        )
    else:
        errores = []

        for campo, lista_errores in form.errors.items():
            for error in lista_errores:
                errores.append(f"{campo}: {error}")

        messages.error(
            request,
            (
                "No se pudieron guardar los cambios. "
                f"{' '.join(errores)}"
            ),
            extra_tags="producto_editado_error",
        )

    return redirect("editar_producto")


@login_required
@require_POST
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    codigo = producto.codigo
    nombre = producto.nombre
    imagen_producto = producto.imagen if producto.imagen else None

    try:
        producto.delete()

        if imagen_producto:
            imagen_producto.delete(save=False)

        messages.success(
            request,
            (
                "Producto eliminado correctamente. "
                f"Producto eliminado: {nombre}. "
                f"Código: {codigo}."
            ),
            extra_tags="producto_eliminado",
        )
    except ProtectedError:
        messages.error(
            request,
            (
                f"No se puede eliminar el producto {codigo} - {nombre} "
                "porque ya está relacionado con una venta registrada."
            ),
            extra_tags="producto_eliminado_error",
        )

    return redirect("editar_producto")


@login_required
def eliminar_productos(request):
    return render(
        request,
        "dashboard/eliminar_productos.html",
    )


@login_required
@require_POST
def confirmar_eliminacion_productos(request):
    productos_ids = request.POST.getlist("productos_ids")

    if not productos_ids:
        messages.error(
            request,
            "Seleccione al menos un producto para eliminar.",
            extra_tags="productos_eliminados_error",
        )
        return redirect("eliminar_productos")

    productos = Producto.objects.filter(
        id__in=productos_ids,
    ).order_by("codigo")

    if not productos.exists():
        messages.error(
            request,
            "No se encontraron los productos seleccionados.",
            extra_tags="productos_eliminados_error",
        )
        return redirect("eliminar_productos")

    eliminados = []
    bloqueados = []

    for producto in productos:
        codigo = producto.codigo
        nombre = producto.nombre
        imagen_producto = producto.imagen if producto.imagen else None

        try:
            producto.delete()

            if imagen_producto:
                imagen_producto.delete(save=False)

            eliminados.append(f"{codigo} - {nombre}")
        except ProtectedError:
            bloqueados.append(f"{codigo} - {nombre}")

    if eliminados:
        if len(eliminados) == 1:
            messages.success(
                request,
                (
                    "Se eliminó correctamente el producto seleccionado: "
                    f"{eliminados[0]}."
                ),
                extra_tags="productos_eliminados",
            )
        else:
            productos_eliminados = "; ".join(eliminados)

            messages.success(
                request,
                (
                    "Se eliminaron correctamente los productos "
                    "seleccionados: "
                    f"{productos_eliminados}."
                ),
                extra_tags="productos_eliminados",
            )

    if bloqueados:
        if len(bloqueados) == 1:
            messages.error(
                request,
                (
                    "No se pudo eliminar el producto seleccionado porque "
                    "está relacionado con una venta registrada: "
                    f"{bloqueados[0]}."
                ),
                extra_tags="productos_eliminados_error",
            )
        else:
            productos_bloqueados = "; ".join(bloqueados)

            messages.error(
                request,
                (
                    "No se pudieron eliminar estos productos porque están "
                    "relacionados con ventas registradas: "
                    f"{productos_bloqueados}."
                ),
                extra_tags="productos_eliminados_error",
            )

    return redirect("eliminar_productos")


@staff_member_required
def finanzas(request):
    return render(
        request,
        "dashboard/finanzas.html",
    )