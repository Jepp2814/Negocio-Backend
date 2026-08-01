from django.db import models
from decimal import Decimal
# 1. PRODUCTO

class Producto(models.Model):

    
    codigo = models.CharField(
        max_length=7,
        unique=True,
        editable=False,
        verbose_name="Código"
    )

    nombre = models.CharField(
        max_length=200,
        verbose_name="Nombre"
        
    )

    
    marca = models.CharField(
        max_length=100,
        verbose_name="Marca"
    )

    modelo = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Modelo"
    )

    categoria = models.ForeignKey(
        'Categoria',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='productos',
        verbose_name="Categoría"
    )
    
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )

    especificaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name="Especificaciones"
    )

    imagen = models.ImageField(
        upload_to="productos/",
        blank=True,
        null=True,
        verbose_name="Imagen Referencial"
    )

    
    costo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Costo"
    )

    precio_venta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Precio de Venta"
    )

    
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name="Stock"
    )

    fecha_llegada = models.DateField(
        blank=True,
        null=True,
        verbose_name="Fecha de Llegada"
    )

    proveedor = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Proveedor"
    )

    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["nombre"]

    @property
    def estado(self):
        if self.stock > 0:
            return "Disponible"
        elif self.fecha_llegada:
            return "Por llegar"
        return "Agotado"

    def generar_codigo(self):

        prefijo = self.nombre[:3].upper()

        ultimo = Producto.objects.filter(
            codigo__startswith=prefijo
        ).order_by('-codigo').first()

        if ultimo:
          numero = int(ultimo.codigo.split('-')[1]) + 1
        else:
          numero = 1

        return f"{prefijo}-{numero:03d}"

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = self.generar_codigo()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    

# 2. PROVEEDOR
class Proveedor(models.Model):

    nombre = models.CharField(max_length=150, unique=True)

    telefono = models.CharField(
        max_length=20,
        blank=True
    )

    correo = models.EmailField(
        blank=True
    )

    direccion = models.CharField(
        max_length=250,
        blank=True
    )

    observaciones = models.TextField(
        blank=True
    )

    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


# 3. CATEGORIA
class Categoria(models.Model):

    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre"
    )

    descripcion = models.TextField(
        blank=True,
        verbose_name="Descripción"
    )

    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

# 4. CLIENTE
class Cliente(models.Model):

    primer_nombre = models.CharField(
        max_length=100,
        verbose_name="Primer Nombre"
    )

    segundo_nombre = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Segundo Nombre"
    )

    primer_apellido = models.CharField(
        max_length=100,
        verbose_name="Primer Apellido"
    )

    segundo_apellido = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Segundo Apellido"
    )

    cedula = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Cédula"
    )

    telefono = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Teléfono"
    )

    correo = models.EmailField(
        blank=True,
        verbose_name="Correo Electrónico"
    )

    direccion = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Dirección"
    )

    observaciones = models.TextField(
        blank=True,
        verbose_name="Observaciones"
    )

    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Registro"
    )

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["primer_apellido", "primer_nombre"]

    def __str__(self):

        nombre = self.primer_nombre

        if self.segundo_nombre:
            nombre += f" {self.segundo_nombre}"

        apellido = self.primer_apellido

        if self.segundo_apellido:
            apellido += f" {self.segundo_apellido}"

        return f"{self.cedula} - {apellido}, {nombre}"

class Venta(models.Model):
    cliente = models.ForeignKey(
        'Cliente',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ventas',
        verbose_name="Cliente"
    )

    fecha = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de venta"
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Subtotal"
    )

    iva = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="IVA"
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Total"
    )

    valor_invertido = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Valor Invertido"
    )

    valor_ganado = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name = "Valor Ganado"
    )

    confirmada = models.BooleanField(
        default=False,
        verbose_name="Confirmada"
    )

    observacion = models.TextField(
        blank=True,
        verbose_name="Observación"
    )

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ["-fecha"]

    def __str__(self):
        return f"Venta #{self.id} - {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}"
    
class DetalleVenta(models.Model):
    venta = models.ForeignKey(
        'Venta',
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name="Venta"
    )

    producto = models.ForeignKey(
        'Producto',
        on_delete=models.PROTECT,
        related_name='detalles_venta',
        verbose_name="Producto"
    )

    cantidad = models.PositiveIntegerField(
        verbose_name="Cantidad"
    )

    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Precio unitario"
    )

    costo_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Costo unitario"
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Subtotal"
    )

    valor_invertido = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Valor Invertido"
    )

    valor_ganado = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Valor ganado"
    )

    class Meta:
        verbose_name = "Detalle de venta"
        verbose_name_plural = "Detalles de venta"

    def save(self, *args, **kwargs):
        self.subtotal = Decimal(self.cantidad) * self.precio_unitario
        self.valor_invertido = Decimal(self.cantidad) * self.costo_unitario
        self.valor_ganado = self.subtotal - self.valor_invertido
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Venta #{self.venta.id} - {self.producto.nombre} x {self.cantidad}"
