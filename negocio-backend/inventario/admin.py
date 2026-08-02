from django.contrib import admin
from .models import (
    Producto,
    Proveedor,
    Categoria,
    Cliente,
    Vehiculo,
    Servicio,
    OrdenTrabajo,
)

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
# 5. VEHÍCULO

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):

    list_display = (
        "placa",
        "marca",
        "modelo",
        "anio",
        "cliente",
    )

    search_fields = (
        "placa",
        "marca",
        "modelo",
        "cliente__primer_nombre",
        "cliente__primer_apellido",
        "cliente__cedula",
    )

    ordering = (
        "placa",
    )
# 6. SERVICIO

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):

    list_display = (
        "vehiculo",
        "fecha_ingreso",
        "estado",
    )

    search_fields = (
        "vehiculo__placa",
        "vehiculo__marca",
        "vehiculo__modelo",
    )

    list_filter = (
        "estado",
        "fecha_ingreso",
    )

    ordering = (
        "-fecha_ingreso",
    )
# 7. ORDEN DE TRABAJO

@admin.register(OrdenTrabajo)
class OrdenTrabajoAdmin(admin.ModelAdmin):

    list_display = (
        "numero",
        "servicio",
        "prioridad",
        "mecanico",
        "estado",
        "fecha_creacion",
    )

    search_fields = (
        "numero",
        "servicio__vehiculo__placa",
        "mecanico",
    )

    list_filter = (
        "estado",
        "prioridad",
    )

    ordering = (
        "-fecha_creacion",
    )