from django.contrib import admin
from .models import Producto, Proveedor, Categoria, Cliente

# 1. PRODUCTO
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):

    list_display = (
        "codigo",
        "nombre",
        "marca",
        "modelo", 
        "precio_venta",
        "stock",
        "estado",
    )

    search_fields = (
        "codigo",
        "nombre",
        "marca",
        "modelo", 
    )

    list_filter = (
        "marca",
    )

    ordering = (
        "nombre",
    )

# 2. PROVEEDOR
@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):

    list_display = (
        "nombre",
        "telefono",
        "correo",
        "activo",
    )

    search_fields = (
        "nombre",
        "telefono",
        "correo",
    )

    ordering = (
        "nombre",
    )

# 2. CATEGORIA
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):

    list_display = (
        "nombre",
        "activo",
    )

    search_fields = (
        "nombre",
    )

    ordering = (
        "nombre",
    )
# 2. CLIENTE
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):

    list_display = (
        "cedula",
        "primer_apellido",
        "segundo_apellido",
        "primer_nombre",
        "segundo_nombre",
        "telefono",
        "activo",
    )

    search_fields = (
        "cedula",
        "primer_nombre",
        "segundo_nombre",
        "primer_apellido",
        "segundo_apellido",
        "telefono",
        "correo",
    )

    list_filter = (
        "activo",
    )

    ordering = (
        "primer_apellido",
        "primer_nombre",
    )

