import os
from pathlib import Path
from sqlalchemy import text
from dotenv import load_dotenv
from app import create_app, db
from app.models.models import User

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la ruta absoluta al directorio actual
current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
instance_dir = current_dir / "instance"
db_path = instance_dir / "scout.db"

print(f"Usando base de datos en: {db_path}")
print(f"La base de datos existe: {db_path.exists()}")

# Verificar que el archivo de base de datos existe
if not os.path.exists(db_path):
    print(f"ERROR: El archivo de base de datos no existe en {db_path}")
    exit(1)

# Crear la aplicación con la configuración correcta
app = create_app()

with app.app_context():
    print('Probando conexión a la base de datos...')
    try:
        result = db.session.execute(text('SELECT 1')).fetchone()
        print(f'Conexión exitosa: {result}')
        
        print('Probando consulta a tabla users...')
        users = User.query.all()
        print(f'Número de usuarios: {len(users)}')
        
        if len(users) == 0:
            print('Creando usuario de prueba...')
            user = User(username='test', email='test@example.com')
            user.set_password('test')
            db.session.add(user)
            db.session.commit()
            print('Usuario creado exitosamente')
        else:
            print('Usuarios existentes:')
            for user in users:
                print(f'  - {user.username} ({user.email})')
        
        print('Prueba completada exitosamente')
    except Exception as e:
        print(f'ERROR: {e}')
        exit(1)