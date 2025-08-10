from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import config  # Usar el nombre correcto del diccionario

# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    
    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.directories import directories_bp
    from app.routes.scout import scout_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(directories_bp, url_prefix='/api/directories')
    app.register_blueprint(scout_bp, url_prefix='/api/scout')
    
    return app