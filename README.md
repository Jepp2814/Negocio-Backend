# negocio-backend

🏢 Proyecto Django para gestión de inventario con API REST

## 📋 Requisitos

- Python 3.8+
- PostgreSQL 12+
- pip

## 🚀 Instalación

### 1. Clonar y preparar entorno

```bash
# Clonar repositorio
git clone <tu-repo>
cd negocio-backend

# Crear ambiente virtual
python -m venv .venv

# Activar ambiente virtual
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

Editar `.env` y configurar credenciales de PostgreSQL:

```env
# Django
DEBUG=True
SECRET_KEY=tu-secret-key-aqui

# Base de datos
DB_NAME=mi_negocio
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
```

### 4. Ejecutar setup inicial

```bash
python setup.py
```

Esto hará automáticamente:
- ✅ Ejecutar migraciones
- ✅ Crear superusuario 'admin' (contraseña definida en ADMIN_PASSWORD del .env)
- ✅ Crear productos de ejemplo

## 🏃 Ejecutar Localmente

### Iniciar servidor (acceso local)

```bash
python manage.py runserver 0.0.0.0:8000
```

**Acceso:**
- 🏠 Home: http://localhost:8000/
- 👨‍💼 Admin: http://localhost:8000/admin/
- 📊 API: http://localhost:8000/api/productos/

**Credenciales Admin:**
- Usuario: `admin`
- Contraseña: `Amypin_1414`

## 🌐 Acceso Remoto con ngrok

Para acceder desde otro equipo/ciudad usando ngrok:

### Paso 1: Instalar ngrok

**Opción A - Python:**
```bash
pip install pyngrok
```

**Opción B - Descargar directo:**
- https://ngrok.com/download
- Descomprimir en C:\ngrok (Windows) o /usr/local/bin (Mac/Linux)

### Paso 2: Crear cuenta ngrok (opcional pero recomendado)

1. Ir a https://ngrok.com/
2. Crear cuenta gratuita
3. Obtener auth token en Dashboard
4. Configurar token: `ngrok config add-authtoken <tu_token>`

### Paso 3: Ejecutar servidor con ngrok

**Terminal 1 - Iniciar Django:**
```bash
python manage.py runserver 0.0.0.0:8000
```

**Terminal 2 - Iniciar ngrok:**

```bash
# Opción A - Usando script Python
python run_ngrok.py

# Opción B - Directamente con ngrok CLI
ngrok http 8000
```

### Paso 4: Acceder desde otro equipo

Ngrok te mostrará una URL pública tipo:
```
https://a1b2c3d4-a1b2.ngrok-free.app
```

Usa esta URL desde cualquier equipo/ciudad:
- 🏠 Home: https://a1b2c3d4-a1b2.ngrok-free.app/
- 👨‍💼 Admin: https://a1b2c3d4-a1b2.ngrok-free.app/admin/
- 📊 API: https://a1b2c3d4-a1b2.ngrok-free.app/api/productos/

## 📡 API REST Endpoints

### Productos

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

# Bajo stock (< 5)
GET /api/productos/bajo_stock/

# Aumentar stock
POST /api/productos/{id}/aumentar_stock/
{"cantidad": 5}

# Disminuir stock
POST /api/productos/{id}/disminuir_stock/
{"cantidad": 2}
```

## 📁 Estructura del Proyecto

```
negocio-backend/
├── core/              # Configuración Django
│   ├── settings.py    # Configuración principal
│   ├── urls.py        # Rutas principales
│   └── wsgi.py
├── inventario/        # App de inventario
│   ├── models.py      # Modelo Producto
│   ├── views.py       # Vistas y ViewSets
│   ├── serializers.py # Serializadores REST
│   └── admin.py       # Admin panel
├── .env              # Variables de entorno (NO subir a git)
├── manage.py         # CLI Django
├── requirements.txt  # Dependencias
├── setup.py         # Script de setup
└── run_ngrok.py     # Script para ejecutar con ngrok
```

## 🔧 Comandos útiles

```bash
# Hacer migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Shell interactivo
python manage.py shell

# Recolectar archivos estáticos
python manage.py collectstatic

# Tests
python manage.py test
```

## ⚠️ Solucionar problemas

### Error: "No such table"
```bash
python manage.py migrate
```

### Error: "Django setup error"
Asegúrate de activar el ambiente virtual:
```bash
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
```

### Error con ngrok: "Connection refused"
```bash
# Verifica que Django esté corriendo
python manage.py runserver 0.0.0.0:8000

# En otra terminal, inicia ngrok
ngrok http 8000
```

### PostgreSQL no conecta
```bash
# Verifica que PostgreSQL esté corriendo
# Windows: Services -> PostgreSQL
# Linux: sudo systemctl status postgresql
# Mac: brew services list | grep postgres

# Verifica credenciales en .env
```

## 📝 Créditos

Usuarios de administrador predefinidos:
- Usuario: `admin` (creado por setup.py)
- Usuario: `admin` (manual si necesitas)

## 📞 Soporte

Para más información:
- Django REST: https://www.django-rest-framework.org/
- ngrok: https://ngrok.com/docs
- PostgreSQL: https://www.postgresql.org/docs/

