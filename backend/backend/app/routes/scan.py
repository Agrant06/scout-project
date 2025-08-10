from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.scan import Scan
from app.models.user import User
import json

bp = Blueprint('scan', __name__, url_prefix='/api/scans')

@bp.route('', methods=['GET'])
@jwt_required()
def get_scans():
    user_id = get_jwt_identity()
    
    # Obtener parámetros de paginación
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status', None)
    
    # Construir consulta
    query = Scan.query.filter_by(user_id=user_id)
    
    if status:
        query = query.filter_by(status=status)
    
    # Ordenar por fecha de creación descendente
    query = query.order_by(Scan.created_at.desc())
    
    # Paginar resultados
    scans = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'scans': [scan.to_dict() for scan in scans.items],
        'total': scans.total,
        'pages': scans.pages,
        'current_page': scans.page
    }), 200

@bp.route('/<scan_id>', methods=['GET'])
@jwt_required()
def get_scan(scan_id):
    user_id = get_jwt_identity()
    
    scan = Scan.query.filter_by(id=scan_id, user_id=user_id).first()
    
    if not scan:
        return jsonify({'error': 'Escaneo no encontrado'}), 404
    
    return jsonify({'scan': scan.to_dict()}), 200

@bp.route('', methods=['POST'])
@jwt_required()
def create_scan():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validar datos requeridos
    required_fields = ['name', 'center_latitude', 'center_longitude', 'radius']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'El campo {field} es requerido'}), 400
    
    # Validar tipos de datos
    try:
        center_latitude = float(data['center_latitude'])
        center_longitude = float(data['center_longitude'])
        radius = float(data['radius'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Latitud, longitud y radio deben ser números válidos'}), 400
    
    # Validar rangos
    if not (-90 <= center_latitude <= 90):
        return jsonify({'error': 'Latitud debe estar entre -90 y 90'}), 400
    
    if not (-180 <= center_longitude <= 180):
        return jsonify({'error': 'Longitud debe estar entre -180 y 180'}), 400
    
    if radius <= 0:
        return jsonify({'error': 'Radio debe ser un número positivo'}), 400
    
    # Crear nuevo escaneo
    try:
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
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al crear escaneo: {str(e)}'}), 500

@bp.route('/<scan_id>', methods=['PUT'])
@jwt_required()
def update_scan(scan_id):
    user_id = get_jwt_identity()
    
    scan = Scan.query.filter_by(id=scan_id, user_id=user_id).first()
    
    if not scan:
        return jsonify({'error': 'Escaneo no encontrado'}), 404
    
    data = request.get_json()
    
    # Actualizar campos permitidos
    if 'name' in data:
        scan.name = data['name']
    if 'description' in data:
        scan.description = data['description']
    if 'center_latitude' in data:
        try:
            scan.center_latitude = float(data['center_latitude'])
            if not (-90 <= scan.center_latitude <= 90):
                return jsonify({'error': 'Latitud debe estar entre -90 y 90'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Latitud debe ser un número válido'}), 400
    
    if 'center_longitude' in data:
        try:
            scan.center_longitude = float(data['center_longitude'])
            if not (-180 <= scan.center_longitude <= 180):
                return jsonify({'error': 'Longitud debe estar entre -180 y 180'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Longitud debe ser un número válido'}), 400
    
    if 'radius' in data:
        try:
            scan.radius = float(data['radius'])
            if scan.radius <= 0:
                return jsonify({'error': 'Radio debe ser un número positivo'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Radio debe ser un número válido'}), 400
    
    if 'categories' in data:
        scan.categories = json.dumps(data['categories'])
    
    if 'status' in data and data['status'] in ['pending', 'in_progress', 'completed']:
        scan.status = data['status']
        if data['status'] == 'completed':
            from datetime import datetime
            scan.completed_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Escaneo actualizado exitosamente',
            'scan': scan.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar escaneo: {str(e)}'}), 500

@bp.route('/<scan_id>', methods=['DELETE'])
@jwt_required()
def delete_scan(scan_id):
    user_id = get_jwt_identity()
    
    scan = Scan.query.filter_by(id=scan_id, user_id=user_id).first()
    
    if not scan:
        return jsonify({'error': 'Escaneo no encontrado'}), 404
    
    try:
        db.session.delete(scan)
        db.session.commit()
        
        return jsonify({'message': 'Escaneo eliminado exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al eliminar escaneo: {str(e)}'}), 500