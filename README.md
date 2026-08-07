# negocio-backend
Proyecto Django para gestion de inventario con API REST.

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
### 3. Actualizar Vsc desde github.
```
1. - git status --short --branch -> revisa estado actual.
2. - git add . -> agregamos y guardamos cambios locales.
3. - git commit -> agregamos y guardamos cambios locales.
4. - git pull origin main -> actualizamos desde el repositorio en github.
5. - git status --short --branch -> confirmamos que todo este actualizado.
```
### 4. Actualizamos Github desde VSC.
1. - git status --short --branch -> verificamos los cambios realizados.
2. - git add . -> preparamos los archivos para el commit.
3. - git commit -> creamos y guardamos los cambios locales.
4. - git push origin main -> enviamos los cambios realizados al Github.

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
