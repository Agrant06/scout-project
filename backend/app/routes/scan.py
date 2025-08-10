from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.scan import Scan
import json

bp = Blueprint('scan', __name__, url_prefix='/api/scans')

@bp.route('', methods=['GET'])
@jwt_required()
def get_scans():
    user_id = get_jwt_identity()
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status', None)
    
    query = Scan.query.filter_by(user_id=user_id)
    
    if status:
        query = query.filter_by(status=status)
    
    scans = query.order_by(Scan.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'scans': [scan.to_dict() for scan in scans.items],
        'total': scans.total,
        'pages': scans.pages,
        'current_page': scans.page
    }), 200

@bp.route('/', methods=['POST'])
@jwt_required()
def create_scan():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    required_fields = ['name', 'center_latitude', 'center_longitude', 'radius']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'El campo {field} es requerido'}), 400
    
    try:
        center_latitude = float(data['center_latitude'])
        center_longitude = float(data['center_longitude'])
        radius = float(data['radius'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Latitud, longitud y radio deben ser números válidos'}), 400
    
    if not (-90 <= center_latitude <= 90):
        return jsonify({'error': 'Latitud debe estar entre -90 y 90'}), 400
    
    if not (-180 <= center_longitude <= 180):
        return jsonify({'error': 'Longitud debe estar entre -180 y 180'}), 400
    
    if radius <= 0:
        return jsonify({'error': 'Radio debe ser un número positivo'}), 400
    
    scan = Scan(
        name=data['name'],
        description=data.get('description', ''),
        center_latitude=center_latitude,
        center_longitude=center_longitude,
        radius=radius,
        categories=json.dumps(data.get('categories', [])),
        user_id=user_id
    )
    
    db.session.add(scan)
    db.session.commit()
    
    return jsonify({
        'message': 'Escaneo creado exitosamente',
        'scan': scan.to_dict()
    }), 201
