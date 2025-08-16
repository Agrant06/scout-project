import os
import sqlite3
from pathlib import Path

# Obtener la ruta absoluta al directorio actual
current_dir = Path(os.path.dirname(os.path.abspath(__file__)))

# Crear la carpeta instance si no existe
instance_dir = current_dir / "instance"
if not instance_dir.exists():
    os.makedirs(instance_dir)
    print(f"Creada carpeta: {instance_dir}")

# Ruta a la base de datos
db_path = instance_dir / "scout.db"
print(f"Usando base de datos en: {db_path}")

# Crear la base de datos manualmente
print("Creando base de datos manualmente...")
conn = sqlite3.connect(str(db_path))
conn.close()
print("Base de datos creada")

# Verificar que se puede abrir la base de datos
try:
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    print(f"Conexión exitosa: {result}")
    conn.close()
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")