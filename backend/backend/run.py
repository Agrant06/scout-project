from flask import Flask, Blueprint, jsonify
from flask_cors import CORS

# Crear aplicación directamente sin importaciones complejas
app = Flask(__name__)
CORS(app)

# Crear blueprints directamente
main_bp = Blueprint('main', __name__)
test_bp = Blueprint('test', __name__, url_prefix='/api/test')

# Definir rutas
@main_bp.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Scout Backend</title></head>
    <body>
        <h1>Scout Backend API</h1>
        <p>Funcionando correctamente</p>
        <p><a href="/api/test">Probar API</a></p>
    </body>
    </html>
    """

@test_bp.route('')
def test():
    return jsonify({"message": "API funcionando correctamente"})

# Registrar blueprints
app.register_blueprint(main_bp)
app.register_blueprint(test_bp)

# Mensajes de depuración
print("Aplicación iniciada")
print("Blueprints registrados:")
for rule in app.url_map.iter_rules():
    print(f"  {rule.rule} -> {rule.endpoint}")

if __name__ == '__main__':
    app.run(debug=True)