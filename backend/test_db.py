import os
import sqlite3
from app import create_app, db

app = create_app()

# Probar con SQLite directamente
print("Probando con SQLite directamente...")
try:
    # Usar una ruta absoluta para evitar problemas
    db_path = os.path.abspath('instance/test.db')
    print(f"Ruta de la base de datos: {db_path}")
    
    # Crear conexión directa con sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("INSERT INTO test (name) VALUES ('test')")
    conn.commit()
    conn.close()
    print("SQLite directo: ÉXITO")
    
    # Eliminar el archivo de prueba
    os.remove(db_path)
    print("Archivo de prueba eliminado")
    
except Exception as e:
    print(f"SQLite directo: ERROR - {e}")

# Probar con SQLAlchemy
print("\nProbando con SQLAlchemy...")
try:
    with app.app_context():
        # Usar una ruta absoluta
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.abspath('instance/test2.db')}"
        db.create_all()
        print("SQLAlchemy: ÉXITO")
        
        # Eliminar el archivo de prueba
        os.remove(os.path.abspath('instance/test2.db'))
        print("Archivo de prueba eliminado")
        
except Exception as e:
    print(f"SQLAlchemy: ERROR - {e}")

# Probar con base de datos en memoria
print("\nProbando con base de datos en memoria...")
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        print("Base de datos en memoria: ÉXITO")
        
except Exception as e:
    print(f"Base de datos en memoria: ERROR - {e}")