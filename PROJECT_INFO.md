# Negocio-Backend — Información del proyecto

## Descripción general

Proyecto backend Django para la gestión de inventario, usuarios y finanzas con API REST.

### Componentes principales
- App `inventario`
  - productos
  - usuarios
  - dashboard
  - API de productos
- App `finance`
  - cuentas financieras
  - categorías financieras
  - movimientos financieros
  - resumen financiero
- Autenticación con Django: login, logout, registro y recuperación de contraseña.
- Soporte para ngrok para exponer el servidor local públicamente.

## Estado actual del repositorio

- Repositorio remoto: `https://github.com/Jepp2814/Negocio-Backend.git`
- Rama activa: `main`
- Último commit: `e7b0d34 Update project info and fix login/profile layout`
- Se actualizó `PROJECT_INFO.md` y se eliminó su exclusión de `.gitignore` para que forme parte del repositorio.
- Se actualizó la pantalla de login y la disposición de perfiles en el panel izquierdo.

## Cambios recientes

- Causa:
  - `inventario/urls.py` tenía dos definiciones separadas de `urlpatterns`.
  - La segunda definición sobrescribía la primera y eliminaba rutas importantes.
- Efecto:
  - `NoReverseMatch` en la página de login / autenticación.
  - Error 500 al cargar algunas vistas.
- Solución:
  - Unificar todas las rutas de `inventario/urls.py` en una sola lista.
  - Eliminar la inclusión duplicada de `inventario.urls` en `core/urls.py`.

## Archivos modificados en la corrección

- `core/urls.py`
- `inventario/views.py`
- `templates/registration/login.html`

## Rutas principales

### `core/urls.py`
- `admin/`
- `login/`
- `logout/`
- `logout-beacon/`
- `accounts/` (autenticación Django)
- `''` incluye `inventario.urls`
- `api/finance/` incluye `finance.urls`

### `inventario/urls.py`
- `''` -> `home`
- `health/`
- `registro/`
- `registro-exitoso/`
- `usuarios/`
- `usuarios/eliminar/<int:user_id>/`
- `api/` -> router de productos
- `logout-beacon/`
- `dashboard/`

### `finance/urls.py`
- `''` -> router de finanzas
- `summary/` -> resumen financiero

## Configuración principal

### `core/settings.py`
- `DEBUG = True`
- `ALLOWED_HOSTS` incluye `localhost`, `127.0.0.1` y dominios de ngrok.
- `CSRF_TRUSTED_ORIGINS` incluye localhost y ngrok.
- `LOGIN_REDIRECT_URL` actualizado a `/dashboard/` para mostrar la vista del dashboard tras iniciar sesión.
- Base de datos por defecto:
  - Engine: `django.db.backends.postgresql`
  - Nombre: `mi_negocio`
  - Usuario: `mi_usuario`
  - Host: `localhost`
  - Puerto: `5432`
- Email configurado para Gmail SMTP.

## Dependencias

Extraídas de `requirements.txt`:
- Django >= 5.2, < 6.0
- djangorestframework >= 3.15
- psycopg2-binary >= 2.9
- python-dotenv >= 1.0
- django-cors-headers >= 4.0
- pyngrok >= 7.0
- Pillow >= 10.0

## Ejecución local

1. Activar entorno virtual:
   - Windows PowerShell:
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar servidor:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```
4. Acceder en el navegador:
   - Home: `http://localhost:8000/`
   - Admin: `http://localhost:8000/admin/`
   - API productos: `http://localhost:8000/api/productos/`

## Uso con ngrok

### Opción recomendada
```bash
python run_ngrok.py
```

### Opción manual
Terminal 1:
```bash
python manage.py runserver 0.0.0.0:8000
```
Terminal 2:
```bash
ngrok http 8000
```

### Token de ngrok
Agregar en `.env`:
```env
NGROK_AUTHTOKEN=tu_token_ngrok
```

## Comandos útiles de Git

```bash
git status --short --branch
git log --oneline --decorate --graph --all
git diff --stat origin/main..main
```

## Notas para otra IA

- El proyecto está listo para seguir modificando desde la rama `main`.
- El archivo `PROJECT_INFO.md` contiene el resumen del estado actual.
- El repositorio remoto disponible es `https://github.com/Jepp2814/Negocio-Backend.git`.
- El error de rutas ya fue corregido.
