from flask import Blueprint, jsonify, request

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return jsonify({
            "message": "Login endpoint - POST",
            "status": "implementación pendiente"
        })
    else:
        return jsonify({
            "message": "Login endpoint - GET no permitido",
            "status": "use POST"
        })