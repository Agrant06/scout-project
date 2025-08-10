from flask import Blueprint, jsonify

bp = Blueprint('test', __name__, url_prefix='/api/test')

@bp.route('')
def test():
    return jsonify({"message": "API funcionando correctamente"})