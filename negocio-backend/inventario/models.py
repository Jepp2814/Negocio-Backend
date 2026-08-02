from django.db import models

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


 # 5. VEHICULO

class Vehiculo(models.Model):

    placa = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Placa"
    )

    marca = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Marca"
    )

    modelo = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Modelo"
    )

    anio = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Año"
    )

    pais = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="País"
    )

    color = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Color"
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="vehiculos"
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        ordering = ["placa"]

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"

# 6. SERVICIO

class Servicio(models.Model):

    ESTADOS = [
        ("RECIBIDO", "Recibido"),
        ("EN PROCESO", "En proceso"),
        ("FINALIZADO", "Finalizado"),
        ("ENTREGADO", "Entregado"),
    ]

    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.PROTECT,
        related_name="servicios",
        verbose_name="Vehículo"
    )

    fecha_ingreso = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de ingreso"
    )

    kilometraje = models.PositiveIntegerField(
        verbose_name="Kilometraje"
    )

    combustible = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Nivel de combustible"
    )

    motivo = models.TextField(
        verbose_name="Motivo del ingreso"
    )

    observaciones = models.TextField(
        blank=True,
        verbose_name="Observaciones"
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="RECIBIDO",
        verbose_name="Estado"
    )

    fecha_entrega = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Fecha de entrega"
    )

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ["-fecha_ingreso"]

    def __str__(self):
        return f"{self.vehiculo.placa} - {self.fecha_ingreso:%d/%m/%Y}"

# 7. ORDEN DE TRABAJO

class OrdenTrabajo(models.Model):

    PRIORIDADES = [
        ("BAJA", "Baja"),
        ("MEDIA", "Media"),
        ("ALTA", "Alta"),
        ("URGENTE", "Urgente"),
    ]

    ESTADOS = [
        ("RECIBIDA", "Recibida"),
        ("EN PROCESO", "En Proceso"),
        ("ESPERA", "Esperando Repuestos"),
        ("FINALIZADA", "Finalizada"),
        ("ENTREGADA", "Entregada"),
    ]

    numero = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        verbose_name="Número OT"
    )

    servicio = models.OneToOneField(
        Servicio,
        on_delete=models.PROTECT,
        related_name="orden_trabajo",
        verbose_name="Servicio"
    )

    prioridad = models.CharField(
        max_length=10,
        choices=PRIORIDADES,
        default="MEDIA",
        verbose_name="Prioridad"
    )

    mecanico = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Mecánico Responsable"
    )

    diagnostico = models.TextField(
        blank=True,
        verbose_name="Diagnóstico"
    )

    trabajo_realizado = models.TextField(
        blank=True,
        verbose_name="Trabajo Realizado"
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="RECIBIDA",
        verbose_name="Estado"
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Orden de Trabajo"
        verbose_name_plural = "Órdenes de Trabajo"
        ordering = ["-fecha_creacion"]
    def generar_numero(self):

        anio = self.fecha_creacion.year if self.fecha_creacion else 2026

        ultima = OrdenTrabajo.objects.filter(
            numero__startswith=f"OT-{anio}"
        ).order_by("-numero").first()

        if ultima:

            consecutivo = int(
                ultima.numero.split("-")[-1]
            ) + 1

        else:

            consecutivo = 1

        return f"OT-{anio}-{consecutivo:06d}"
    def save(self, *args, **kwargs):

        if not self.numero:
            self.numero = self.generar_numero()

        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.numero} - {self.servicio.vehiculo.placa}"
    

    
