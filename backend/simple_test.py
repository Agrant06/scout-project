import os
import sqlite3
from pathlib import Path
from sqlalchemy import text

# Obtener la ruta absoluta al directorio actual
current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
db_path = current_dir / "instance" / "scout.db"

print(f"Ruta de la base de datos: {db_path}")
print(f"La base de datos existe: {db_path.exists()}")

if db_path.exists():
    try:
        # Probar conexión directa con sqlite3
        print("Probando conexión directa con sqlite3...")
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tablas en la base de datos: {tables}")
        conn.close()
        
        # Probar con SQLAlchemy
        print("Probando conexión con SQLAlchemy...")
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db = SQLAlchemy(app)
        
        with app.app_context():
            result = db.session.execute(text('SELECT 1')).fetchone()
            print(f"Conexión SQLAlchemy exitosa: {result}")
            
    except Exception as e:
        print(f"Error: {e}")
else:
    print("La base de datos no existe")