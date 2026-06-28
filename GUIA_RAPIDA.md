# Guía rápida de ejecución

## Ejecución local

1. Entrar al proyecto
   ```bash
   cd negocio-backend
   .venv\Scripts\activate
   ```

2. Iniciar el servidor
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

Acceso local:
- Admin: `http://localhost:8000/admin/`
  - Usuario: admin
  - Contraseña: la que definiste en el archivo `.env`
- API: `http://localhost:8000/api/productos/`

## Acceso remoto con ngrok

1. En una terminal inicia Django
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

2. En otra terminal inicia ngrok
   ```bash
   python run_ngrok.py
   ```
   O bien:
   ```bash
   ngrok http 8000
   ```

Acceso remoto:
- Admin: `https://tu-url-ngrok.ngrok-free.app/admin/`
- API: `https://tu-url-ngrok.ngrok-free.app/api/productos/`

Importante: comparte solo la URL HTTPS con tu otro equipo.

## Pasos iniciales

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Configurar variables:
   Edita el archivo .env con tus datos reales.

3. Configuración inicial:
   ```bash
   python setup.py
   ```

4. Iniciar servidor:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

## Solución de problemas

- Puerto ocupado:
  ```bash
  python manage.py runserver 0.0.0.0:8001
  ```

- Error de base de datos:
  Verifica las credenciales en .env y que PostgreSQL esté corriendo.

- Ngrok no encontrado:
  ```bash
  pip install pyngrok
  ```

- Módulo no encontrado:
  ```bash
  .venv\Scripts\activate
  pip install -r requirements.txt
  ```
