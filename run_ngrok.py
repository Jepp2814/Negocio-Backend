import os
import re
import subprocess
import time
from pathlib import Path
from dotenv import load_dotenv
from pyngrok import ngrok

load_dotenv()


def main():
    print("=" * 60)
    print("SERVIDOR DJANGO CON NGROK")
    print("=" * 60)

    django_port = 8000
    print(f"\n1️⃣  Iniciando Django en puerto {django_port}...")
    django_proc = subprocess.Popen(
        ['python', 'manage.py', 'runserver', f'0.0.0.0:{django_port}'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    time.sleep(2)

    if django_proc.poll() is not None:
        print("❌ Django no pudo arrancar. Revisa errores de configuración.")
        return

    print("✅ Django iniciado")

    try:
        auth_token = os.environ.get('NGROK_AUTHTOKEN')
        if auth_token:
            ngrok.set_auth_token(auth_token)

        # Cerrar túneles existentes que apunten al mismo puerto para evitar duplicados
        try:
            existing = ngrok.get_tunnels()
            for t in existing:
                addr = str(getattr(t, 'addr', ''))
                if addr.endswith(f":{django_port}") or addr in (f"127.0.0.1:{django_port}", f"localhost:{django_port}"):
                    try:
                        ngrok.disconnect(t.public_url)
                    except Exception:
                        # Si no se puede desconectar uno, continuar
                        pass
        except Exception:
            # Si no se pueden listar túneles, continuar de todas formas
            pass

        # Crear un único túnel HTTP explícito al puerto de Django
        tunnel = ngrok.connect(django_port, "http")
        public_url = tunnel.public_url

        env_path = Path('.env')
        env_content = env_path.read_text(encoding='utf-8') if env_path.exists() else ''

        nueva_linea = f'NGROK_URL={public_url}'
        if re.search(r'^#?\s*NGROK_URL=.*$', env_content, flags=re.MULTILINE):
            env_content = re.sub(
                r'^#?\s*NGROK_URL=.*$',
                nueva_linea,
                env_content,
                flags=re.MULTILINE
            )
        else:
            env_content = env_content.rstrip('\n') + f'\n{nueva_linea}\n'

        env_path.write_text(env_content, encoding='utf-8')
        print("✅ NGROK_URL guardada en .env")
        print("✅ ngrok conectado")

        print(f"\n🌐 RED PÚBLICA: {public_url}")
        print(f"📍 RED LOCAL:   http://localhost:{django_port}")
        print("\n⏰ Presiona Ctrl+C para detener\n")

        try:
            ngrok.get_ngrok_process().proc.wait()
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo servicios...")
            ngrok.kill()
            django_proc.terminate()
            print("✅ Todo detenido correctamente")

    except Exception as e:
        print(f"❌ Error con ngrok: {e}")
        print("   Asegúrate de tener NGROK_AUTHTOKEN en tu .env")
        django_proc.terminate()
        return False

    return True


if __name__ == '__main__':
    main()