import sys
import os

# Agregar el directorio padre al sys.path para poder importar los módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import user, business, scan, diagnosis, recommendation

app = create_app()

with app.app_context():
    db.create_all()
    print("Base de datos inicializada correctamente")