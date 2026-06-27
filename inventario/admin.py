from django.contrib import admin
from .models import Producto, Proveedor, Categoria

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
    
