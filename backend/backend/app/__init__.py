from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config.config import config

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Importar modelos
    from app.models import user, business, scan, diagnosis, recommendation
    
    # Importar blueprints
    from app.routes.auth import bp as auth_bp
    from app.routes.main import bp as main_bp
    from app.routes.test import bp as test_bp
    
    # Registrar blueprints con mensajes de depuración
    print("Registrando blueprints...")
    
    print("Registrando auth_bp...")
    app.register_blueprint(auth_bp)
    print("auth_bp registrado correctamente")
    
    print("Registrando main_bp...")
    app.register_blueprint(main_bp)
    print("main_bp registrado correctamente")
    
    print("Registrando test_bp...")
    app.register_blueprint(test_bp)
    print("test_bp registrado correctamente")
    
    print("Todos los blueprints registrados correctamente")
    
    # Imprimir rutas registradas
    print("Rutas registradas:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.rule} -> {rule.endpoint}")
    
    return app