import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la ruta absoluta al directorio actual
current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
instance_dir = current_dir / "instance"
db_path = instance_dir / "scout.db"

print(f"Directorio actual: {current_dir}")
print(f"Directorio instance: {instance_dir}")
print(f"Ruta de la base de datos: {db_path}")
print(f"DATABASE_URL desde entorno: {os.environ.get('DATABASE_URL')}")
print(f"La base de datos existe: {db_path.exists()}")

# Verificar que el archivo .env existe
env_file = current_dir / ".env"
print(f"Archivo .env existe: {env_file.exists()}")

if env_file.exists():
    print(f"Contenido de .env:")
    with open(env_file, 'r') as f:
        print(f.read())