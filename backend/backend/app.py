from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Crear aplicación
app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scout.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# Rutas principales
@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Scout Backend API</title></head>
    <body>
        <h1>Scout Backend API</h1>
        <p>Funcionando correctamente</p>
        <p><a href="/api/test">Probar API</a></p>
        <p><a href="/api/auth/login">Login</a></p>
    </body>
    </html>
    """

@app.route('/api/test')
def test():
    return jsonify({
        "message": "API funcionando correctamente",
        "status": "ok"
    })

@app.route('/api/auth/login', methods=['GET', 'POST'])
def api_login():
    return jsonify({
        "message": "Login endpoint funcionando",
        "status": "ok"
    })

# Mensajes de depuración
print("Aplicación iniciada")
print("Rutas registradas:")
for rule in app.url_map.iter_rules():
    print(f"  {rule.rule} -> {rule.endpoint}")
    print(f"    Métodos: {rule.methods}")

if __name__ == '__main__':
    app.run(debug=True)