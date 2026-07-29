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
### 3. Actualizar en github.
```bash
#1ero trae el original con:
git pull --rebase origin main
#2do actualiza el codigo:
git push origin main
```

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
- Contraseña: Jepp1995

## Acceso Remoto con ngrok

### Opcion A - Automatico (recomendado)

Inicia Django y ngrok en un solo comando:

```bash
python run_ngrok.py
```

Veras en la terminal:
URL PUBLICA : https://xxxx.ngrok-free.app
Admin : https://xxxx.ngrok-free.app/admin/
API : https://xxxx.ngrok-free.app/api/productos/

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
## Soporte

- Django REST Framework: https://www.django-rest-framework.org/
- ngrok: https://ngrok.com/docs
- PostgreSQL: https://www.postgresql.org/docs/
