import os
from app import create_app, db
from app.models.models import User, Dealership, Lead, ScoutScan, ScoutBusiness, ScoutDiagnostic

def init_db():
    # Crear la aplicación con la configuración de desarrollo
    app = create_app('development')
    
    # Obtener la ruta de la base de datos
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    db_path = db_uri.replace('sqlite:///', '')
    
    print(f"Configuración de la base de datos: {db_uri}")
    print(f"Ruta absoluta: {os.path.abspath(db_path)}")
    
    # Asegurar que el directorio exista
    db_dir = os.path.dirname(os.path.abspath(db_path))
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        print(f"Directorio creado: {db_dir}")
    
    # Crear todas las tablas
    with app.app_context():
        db.create_all()
        print("Base de datos creada exitosamente")
        
        # Crear un usuario de prueba
        if not User.query.filter_by(username='test').first():
            user = User(username='test', email='test@example.com')
            user.set_password('test')
            db.session.add(user)
            db.session.commit()
            print("Usuario de prueba creado")
        else:
            print("Usuario de prueba ya existe")

if __name__ == '__main__':
    init_db()