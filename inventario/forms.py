from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.text import slugify

from .models import Producto


solo_letras = RegexValidator(
    regex=r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$",
    message="Este campo solo acepta letras y espacios.",
)


def limpiar_texto(texto):
    return slugify(texto).replace("-", " ").split()


def generar_sugerencias_username(nombres, apellidos, fecha_nacimiento=None):
    nombres_limpios = limpiar_texto(nombres)
    apellidos_limpios = limpiar_texto(apellidos)

    sugerencias = []

    if not nombres_limpios or not apellidos_limpios:
        return sugerencias

    inicial_nombre_1 = (
        nombres_limpios[0][0]
        if len(nombres_limpios) > 0
        else ""
    )
    inicial_nombre_2 = (
        nombres_limpios[1][0]
        if len(nombres_limpios) > 1
        else ""
    )
    inicial_apellido_1 = (
        apellidos_limpios[0][0]
        if len(apellidos_limpios) > 0
        else ""
    )
    inicial_apellido_2 = (
        apellidos_limpios[1][0]
        if len(apellidos_limpios) > 1
        else ""
    )

    primer_nombre = nombres_limpios[0] if nombres_limpios else ""
    primer_apellido = apellidos_limpios[0] if apellidos_limpios else ""
    segundo_apellido = (
        apellidos_limpios[1]
        if len(apellidos_limpios) > 1
        else ""
    )

    base_corta = (
        f"{inicial_nombre_1}{primer_apellido}{inicial_apellido_2}".lower()
    )
    base_iniciales = (
        f"{inicial_nombre_1}{inicial_nombre_2}"
        f"{inicial_apellido_1}{inicial_apellido_2}"
    )
    base_nombre = f"{primer_nombre[:2]}{primer_apellido[:2]}".lower()

    if base_corta:
        sugerencias.append(base_corta)

    if base_iniciales:
        sugerencias.append(base_iniciales.lower())
        sugerencias.append(base_iniciales.upper())
        sugerencias.append(base_iniciales.capitalize())

    if primer_nombre and primer_apellido:
        sugerencias.append(
            f"{primer_nombre[0]}{primer_apellido}{segundo_apellido[:1]}".lower()
        )

    if fecha_nacimiento:
        dia = f"{fecha_nacimiento.day:02d}"
        mes = f"{fecha_nacimiento.month:02d}"
        anio = str(fecha_nacimiento.year)
        anio_corto = anio[-2:]

        if base_iniciales:
            sugerencias.append(f"{base_iniciales.capitalize()}{anio}")
            sugerencias.append(f"{base_iniciales.upper()}{dia}{anio_corto}")
            sugerencias.append(f"{base_iniciales.lower()}{mes}{anio_corto}")

        if base_nombre:
            sugerencias.append(f"{base_nombre}{anio}")
            sugerencias.append(f"{base_nombre}{dia}{anio_corto}")

    sugerencias_unicas = []

    for sugerencia in sugerencias:
        if sugerencia and sugerencia not in sugerencias_unicas:
            sugerencias_unicas.append(sugerencia)

    disponibles = []

    for sugerencia in sugerencias_unicas:
        if not User.objects.filter(username=sugerencia).exists():
            disponibles.append(sugerencia)
        else:
            contador = 1

            while User.objects.filter(
                username=f"{sugerencia}{contador}"
            ).exists():
                contador += 1

            disponibles.append(f"{sugerencia}{contador}")

    return disponibles[:8]


class RegistroUsuarioForm(UserCreationForm):
    first_name = forms.CharField(
        label="Nombres",
        max_length=150,
        required=True,
        validators=[solo_letras],
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ingrese sus nombres completos",
            }
        ),
    )

    last_name = forms.CharField(
        label="Apellidos",
        max_length=150,
        required=True,
        validators=[solo_letras],
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ingrese sus apellidos completos",
            }
        ),
    )

    fecha_nacimiento = forms.DateField(
        label="Fecha de nacimiento",
        required=True,
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        ),
    )

    pais = forms.CharField(
        label="País",
        max_length=100,
        required=True,
        validators=[solo_letras],
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ingrese su país de residencia",
            }
        ),
    )

    ciudad = forms.CharField(
        label="Ciudad",
        max_length=100,
        required=True,
        validators=[solo_letras],
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ingrese su ciudad de residencia",
            }
        ),
    )

    email = forms.EmailField(
        label="Correo electrónico",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Ingrese su correo electrónico",
            }
        ),
    )

    celular = forms.CharField(
        label="Celular",
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ingrese su número celular",
            }
        ),
    )

    username = forms.CharField(
        label="Nombre de usuario",
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": (
                    "Escriba un nombre de usuario o use una sugerencia"
                ),
            }
        ),
    )

    password1 = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Ingrese su contraseña",
            }
        ),
    )

    password2 = forms.CharField(
        label="Confirmar contraseña",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirme su contraseña",
            }
        ),
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sugerencias_username = []
        self.fields["username"].help_text = (
            "Ingrese un usuario que no haya sido utilizado."
        )
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if not email:
            raise forms.ValidationError("Este campo es obligatorio.")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Ese correo electrónico ya está registrado. Intente con otro."
            )

        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if not username:
            raise forms.ValidationError("Este campo es obligatorio.")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Ese nombre de usuario ya está en uso. Intente con otro."
            )

        return username

    def clean_celular(self):
        celular = self.cleaned_data.get("celular")

        if not celular:
            raise forms.ValidationError("Este campo es obligatorio.")

        return celular

    def clean(self):
        cleaned_data = super().clean()
        nombres = cleaned_data.get("first_name")
        apellidos = cleaned_data.get("last_name")
        fecha_nacimiento = cleaned_data.get("fecha_nacimiento")
        username = cleaned_data.get("username")

        if nombres and apellidos and fecha_nacimiento:
            self.sugerencias_username = generar_sugerencias_username(
                nombres,
                apellidos,
                fecha_nacimiento,
            )

        if not username and self.sugerencias_username:
            self.add_error(
                "username",
                (
                    "Utilice un usuario de las opciones sugeridas: "
                    f"{', '.join(self.sugerencias_username)}"
                ),
            )

        return cleaned_data


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            "nombre",
            "marca",
            "modelo",
            "especificaciones",
            "imagen",
            "costo",
            "costo_caja",
            "precio_venta",
            "precio_venta_caja",
            "stock",
            "proveedor",
        ]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese el nombre del producto",
                }
            ),
            "marca": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese la marca",
                }
            ),
            "modelo": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese el modelo",
                }
            ),
            "especificaciones": forms.Textarea(
                attrs={
                    "placeholder": "Ingrese las especificaciones",
                    "rows": 3,
                }
            ),
            "imagen": forms.ClearableFileInput(
                attrs={
                    "accept": "image/*",
                }
            ),
            "costo": forms.NumberInput(
                attrs={
                    "placeholder": "0.00",
                    "min": "0",
                    "step": "0.01",
                }
            ),
            "costo_caja": forms.NumberInput(
                attrs={
                    "placeholder": "0.00",
                    "min": "0",
                    "step": "0.01",
                }
            ),
            "precio_venta": forms.NumberInput(
                attrs={
                    "placeholder": "0.00",
                    "min": "0",
                    "step": "0.01",
                }
            ),
            "precio_venta_caja": forms.NumberInput(
                attrs={
                    "placeholder": "0.00",
                    "min": "0",
                    "step": "0.01",
                }
            ),
            "stock": forms.NumberInput(
                attrs={
                    "placeholder": "0",
                    "min": "0",
                }
            ),
            "proveedor": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese el proveedor",
                }
            ),
        }


class ProductoEditarForm(forms.Form):
    codigo = forms.CharField(
        label="Código",
        max_length=7,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ejemplo: ACE-001",
                "maxlength": "7",
            }
        ),
    )

    nombre = forms.CharField(
        label="Nombre",
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ingrese el nombre del producto",
            }
        ),
    )

    marca = forms.CharField(
        label="Marca",
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ingrese la marca",
            }
        ),
    )

    modelo = forms.CharField(
        label="Modelo",
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ingrese el modelo",
            }
        ),
    )

    proveedor = forms.CharField(
        label="Proveedor",
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ingrese el proveedor",
            }
        ),
    )

    costo = forms.DecimalField(
        label="Costo por unidad",
        max_digits=10,
        decimal_places=2,
        required=False,
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                "placeholder": "0.00",
                "min": "0",
                "step": "0.01",
            }
        ),
    )

    costo_caja = forms.DecimalField(
        label="Costo por caja",
        max_digits=10,
        decimal_places=2,
        required=False,
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                "placeholder": "0.00",
                "min": "0",
                "step": "0.01",
            }
        ),
    )

    precio_venta = forms.DecimalField(
        label="Precio de venta por unidad",
        max_digits=10,
        decimal_places=2,
        required=True,
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                "placeholder": "0.00",
                "min": "0",
                "step": "0.01",
            }
        ),
    )

    precio_venta_caja = forms.DecimalField(
        label="Precio de venta por caja",
        max_digits=10,
        decimal_places=2,
        required=False,
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                "placeholder": "0.00",
                "min": "0",
                "step": "0.01",
            }
        ),
    )

    stock = forms.IntegerField(
        label="Stock",
        required=True,
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                "placeholder": "0",
                "min": "0",
            }
        ),
    )

    especificaciones = forms.CharField(
        label="Especificaciones",
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Ingrese las especificaciones",
                "rows": 5,
            }
        ),
    )

    imagen = forms.ImageField(
        label="Imagen referencial",
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "accept": "image/*",
            }
        ),
    )

    def __init__(self, *args, producto=None, **kwargs):
        self.producto = producto
        super().__init__(*args, **kwargs)

        if producto and not self.is_bound:
            self.initial.update({
                "codigo": producto.codigo,
                "nombre": producto.nombre,
                "marca": producto.marca or "",
                "modelo": producto.modelo or "",
                "proveedor": producto.proveedor or "",
                "costo": producto.costo,
                "costo_caja": producto.costo_caja,
                "precio_venta": producto.precio_venta,
                "precio_venta_caja": producto.precio_venta_caja,
                "stock": producto.stock,
                "especificaciones": producto.especificaciones or "",
            })

    def clean_codigo(self):
        codigo = self.cleaned_data["codigo"].strip().upper()

        producto_existente = Producto.objects.filter(codigo=codigo)

        if self.producto:
            producto_existente = producto_existente.exclude(
                pk=self.producto.pk
            )

        if producto_existente.exists():
            raise forms.ValidationError(
                "Este código ya pertenece a otro producto."
            )

        return codigo