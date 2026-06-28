# negocio-backend

Proyecto Django para gestion de inventario con API REST.

## Requisitos

- Python 3.10+
- PostgreSQL 12+
- pip

## Instalacion

### 1. Clonar y preparar entorno

```bash
git clone https://github.com/Jepp2814/Negocio-Backend.git
cd negocio-backend

python -m venv .venv

# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Crea un archivo `.env` en la raiz del proyecto con este contenido:

```env
DEBUG=True
SECRET_KEY=genera-una-clave-con-el-comando-de-abajo

DB_ENGINE=django.db.backends.postgresql
DB_NAME=mi_negocio
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000

ADMIN_PASSWORD=tu_contraseña_de_admin

NGROK_AUTHTOKEN=tu_token_de_ngrok
```

Para generar un SECRET_KEY seguro:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Ejecutar setup inicial

```bash
python setup.py
```

Esto hace automaticamente:
- Ejecutar migraciones
- Crear superusuario Jepp con la contraseña definida en ADMIN_PASSWORD
- Crear productos de ejemplo

## Ejecucion Local

```bash
python manage.py runserver 0.0.0.0:8000
```

Acceso:
- Home: http://localhost:8000/
- Admin: http://localhost:8000/admin/
- API: http://localhost:8000/api/productos/

Credenciales Admin:
- Usuario: Jepp
- Contraseña: la definida en ADMIN_PASSWORD del archivo .env

## Acceso Remoto con ngrok

### Opcion A - Automatico (recomendado)

Inicia Django y ngrok en un solo comando:

```bash
python run_ngrok.py
```

Veras una URL publica como:
URL PUBLICA: https://xxxx.ngrok-free.app
Admin: https://xxxx.ngrok-free.app/admin/
API: https://xxxx.ngrok-free.app/api/productos/

text

Comparte esa URL con tu otro equipo.

### Opcion B - Manual (dos terminales)

Terminal 1:
```bash
python manage.py runserver 0.0.0.0:8000
```

Terminal 2:
```bash
ngrok http 8000
```

### Configurar ngrok authtoken (primera vez)

1. Crear cuenta gratuita en https://ngrok.com/
2. Obtener el token en https://dashboard.ngrok.com
3. Agregarlo en el archivo .env:

```env
NGROK_AUTHTOKEN=tu_token_aqui
```

## Cambios realizados en este proyecto

### requirements.txt
- Corregida version de Django de 6.0.4 a 5.2
- Corregido nombre de djangorestframework (mayusculas incorrectas)

### core/settings.py
- Eliminada contraseña hardcodeada en DB_PASSWORD
- Corregido validador CommonCommonPasswordValidator a CommonPasswordValidator
- Cambiado idioma a es-ec (español Ecuador)
- Cambiada zona horaria a America/Guayaquil
- Agregado DEFAULT_AUTO_FIELD = BigAutoField

### setup.py
- Carga correcta del archivo .env antes de iniciar Django
- Eliminada contraseña admin123 hardcodeada
- Contraseña leida desde variable ADMIN_PASSWORD del .env
- Usuario administrador configurado como Jepp

### run_ngrok.py
- Ahora inicia Django automaticamente antes de conectar ngrok
- Guarda la URL publica en el archivo .env automaticamente
- Lee NGROK_AUTHTOKEN desde el .env
- Maneja correctamente Ctrl+C para detener todos los servicios

### inventario/serializers.py
- Corregida indentacion incorrecta en class Meta

### inventario/admin.py
- Eliminado list_filter por stock (no generaba filtros utiles)
- Agregado campo created_at en list_display
- Agregado ordering por fecha de creacion
- Agregado readonly_fields para fechas

## API REST Endpoints

```bash
# Listar todos
GET /api/productos/

# Crear
POST /api/productos/
{
  "codigo": "PROD001",
  "nombre": "Producto",
  "costo": 100.00,
  "precio_venta": 150.00,
  "stock": 10
}

# Ver detalle
GET /api/productos/{id}/

# Actualizar
PUT /api/productos/{id}/

# Eliminar
DELETE /api/productos/{id}/

# Buscar
GET /api/productos/?search=laptop

# Bajo stock
GET /api/productos/bajo_stock/

# Aumentar stock
POST /api/productos/{id}/aumentar_stock/
{"cantidad": 5}

# Disminuir stock
POST /api/productos/{id}/disminuir_stock/
{"cantidad": 2}
```

## Estructura del Proyecto
negocio-backend/
├── core/
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── inventario/
│ ├── models.py
│ ├── views.py
│ ├── serializers.py
│ ├── urls.py
│ └── admin.py
├── .env (NO subir a git)
├── .gitignore
├── manage.py
├── requirements.txt
├── setup.py
├── run_ngrok.py
├── README.md
└── GUIA_RAPIDA.md

text

## Comandos utiles

```bash
# Migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Shell interactivo
python manage.py shell

# Tests
python manage.py test
```

## Solucionar problemas

### Error: "No such table"
```bash
python manage.py migrate
```

### Error: venv no activo
```bash
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
```

### Error con ngrok: "Connection refused"
```bash
python manage.py runserver 0.0.0.0:8000
ngrok http 8000
```

### PostgreSQL no conecta
```bash
# Windows: Services -> PostgreSQL -> Iniciar
# Linux: sudo systemctl start postgresql
# Verificar credenciales en .env
```

### Puerto ocupado
```bash
python manage.py runserver 0.0.0.0:8001
```

## Soporte

- Django REST Framework: https://www.django-rest-framework.org/
- ngrok: https://ngrok.com/docs
- PostgreSQL: https://www.postgresql.org/docs/