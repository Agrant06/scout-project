from app import create_app, db
import os

app = create_app()

def init_db():
    with app.app_context():
        # Verificar si la base de datos existe
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        db_dir = os.path.dirname(db_path)
        
        # Crear el directorio si no existe
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        # Crear todas las tablas
        db.create_all()
        print("Base de datos inicializada correctamente")
        print(f"Ruta de la base de datos: {db_path}")

if __name__ == '__main__':
    init_db()