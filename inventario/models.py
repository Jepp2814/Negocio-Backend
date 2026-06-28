from django.db import models
from django.core.exceptions import ValidationError

class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def clean(self):
        if self.precio_venta < self.costo:
            raise ValidationError('El precio de venta no puede ser menor al costo.')
        if self.stock < 0:
            raise ValidationError('El stock no puede ser negativo.')

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
