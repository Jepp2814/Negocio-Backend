from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'stock', 'costo', 'precio_venta']
    list_filter = ['stock']
    search_fields = ['codigo', 'nombre']
