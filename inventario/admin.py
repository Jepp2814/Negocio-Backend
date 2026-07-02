from django.contrib import admin
from .models import Producto

# 1. PRODUCTO
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'stock', 'precio_venta', 'created_at']
    search_fields = ['codigo', 'nombre']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
