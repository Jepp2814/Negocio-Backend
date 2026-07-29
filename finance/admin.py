from django.contrib import admin
from .models import Cuenta, CategoriaFinanciera, MovimientoFinanciero

@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'tipo', 'saldo_inicial')
    search_fields = ('nombre',)
    list_filter = ('tipo',)

@admin.register(CategoriaFinanciera)
class CategoriaFinancieraAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'tipo')
    search_fields = ('nombre',)
    list_filter = ('tipo',)

@admin.register(MovimientoFinanciero)
class MovimientoFinancieroAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo', 'monto', 'fecha', 'cuenta', 'categoria')
    search_fields = ('desripcion',)
    list_filter = ('tipo', 'fecha', 'cuenta', 'categoria')

