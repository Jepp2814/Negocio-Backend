import os
import sys
import django
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User


def main():
    print("=" * 60)
    print("CONFIGURACIÓN INICIAL DEL PROYECTO")
    print("=" * 60)

    print("\n1️⃣  Ejecutando migraciones...")
    call_command('migrate')
    print("✅ Migraciones completadas")

    print("\n2️⃣  Verificando superusuario...")
    if not User.objects.filter(username='Jepp').exists():
        User.objects.create_superuser('Jepp', 'admin@example.com', 'Jepp1995')
        print("✅ Superusuario 'Jepp' creado")
    else:
        print("ℹ️  Superusuario 'Jepp' ya existe")

    print("\n3️⃣  Verificando datos de ejemplo...")
    from inventario.models import Producto

    if not Producto.objects.exists():
        productos_ejemplo = [
            {
                'codigo': 'PROD001',
                'nombre': 'Laptop Dell',
                'costo': 400.00,
                'precio_venta': 650.00,
                'stock': 5,
            },
            {
                'codigo': 'PROD002',
                'nombre': 'Mouse Logitech',
                'costo': 15.00,
                'precio_venta': 25.00,
                'stock': 50,
            },
            {
                'codigo': 'PROD003',
                'nombre': 'Teclado Mecánico',
                'costo': 80.00,
                'precio_venta': 120.00,
                'stock': 2,
            },
        ]
        for prod in productos_ejemplo:
            Producto.objects.create(**prod)
        print("✅ Productos de ejemplo creados")
    else:
        print(f"ℹ️  Ya existen {Producto.objects.count()} productos")

    print("\n" + "=" * 60)
    print("🚀 CONFIGURACIÓN COMPLETADA")
    print("=" * 60)
    print("\n📋 Próximos pasos:")
    print("   1. Iniciar servidor: python manage.py runserver 0.0.0.0:8000")
    print("   2. Admin: http://localhost:8000/admin/")
    print("   3. API: http://localhost:8000/api/productos/")
    print("\n")


if __name__ == '__main__':
    main()