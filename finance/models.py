from django.db import models
from django.utils import timezone

class Cuenta(models.Model):
    TIPO_CUENTA_CHOICES = [
        ('caja', 'Caja'),
        ('banco', 'Banco'),
        ('ahorro', 'Ahorro'),
        ('otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CUENTA_CHOICES, default='caja')
    saldo_inicial = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    activa = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class CategoriaFinanciera(models.Model):
    TIPO_CHOICES = [
        ('ingres', 'Ingreso'),
        ('egreso', 'Egreso'),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

    class Meta:
        verbose_name = 'Categoría financiera'
        verbose_name_plural = 'Categorías financieras'
        unique_together = ('nombre', 'tipo')
        ordering = ['tipo', 'nombre']

    def __str__(self):
        return f'{self.nombre} ({self.tipo})'

class MovimientoFinanciero(models.Model):
    TIPO_CHOICES = [
        ('ingreso', 'Ingresos'),
        ('egreso', 'Egreso'),
    ]

    ORIGEN_CHOICES = [
        ('venta_producto', 'Venta de producto'),
        ('servicio_mantenimiento', 'Servicio de mantenimiento'),
        ('compra', 'Cpompra'),
        ('gasto_manual', 'Gasto manual'),
        ('otro', 'Otro'),
    ]

    cuenta = models.ForeignKey(Cuenta, on_delete=models.PROTECT, related_name='movimientos')
    categoria = models.ForeignKey(CategoriaFinanciera, on_delete=models.PROTECT, related_name='movimientos')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    origen = models.CharField(max_length=30, choices=ORIGEN_CHOICES, default='otro')
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    descripcion = models.TextField(blank=True)
    referencia = models.CharField(max_length=100, blank=True)
    fecha = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Movimiento financiero'
        verbose_name_plural = 'Movimientos financieros'
        ordering = ['-fecha', '-id']

    def __str__(self):
        return f'{self.tipo} - {self.monto} - {self.origen}'
    