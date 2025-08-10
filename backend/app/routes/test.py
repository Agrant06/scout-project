from flask import Blueprint, jsonify

bp = Blueprint('test', __name__, url_prefix='/api/test')

@bp.route('', methods=['GET'])
def test():
    return jsonify({
        'message': 'API funcionando correctamente',
        'status': 'ok',
        'endpoints': {
            'auth': '/api/auth/login',
            'businesses': '/api/businesses',
            'diagnosis': '/api/diagnosis'
        }
    })