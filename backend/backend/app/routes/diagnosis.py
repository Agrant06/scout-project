from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.diagnosis import Diagnosis
from app.models.business import Business
from app.models.scan import Scan
from app.models.user import User
import json

bp = Blueprint('diagnosis', __name__, url_prefix='/api/diagnoses')

@bp.route('', methods=['GET'])
@jwt_required()
def get_diagnoses():
    user_id = get_jwt_identity()
    
    # Obtener parámetros de paginación y filtrado
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    business_id = request.args.get('business_id', None)
    scan_id = request.args.get('scan_id', None)
    
    # Construir consulta
    query = Diagnosis.query.filter_by(user_id=user_id)
    
    if business_id:
        query = query.filter_by(business_id=business_id)
    
    if scan_id:
        query = query.filter_by(scan_id=scan_id)
    
    # Ordenar por fecha de creación descendente
    query = query.order_by(Diagnosis.created_at.desc())
    
    # Paginar resultados
    diagnoses = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'diagnoses': [diagnosis.to_dict() for diagnosis in diagnoses.items],
        'total': diagnoses.total,
        'pages': diagnoses.pages,
        'current_page': diagnoses.page
    }), 200

@bp.route('/<diagnosis_id>', methods=['GET'])
@jwt_required()
def get_diagnosis(diagnosis_id):
    user_id = get_jwt_identity()
    
    diagnosis = Diagnosis.query.filter_by(id=diagnosis_id, user_id=user_id).first()
    
    if not diagnosis:
        return jsonify({'error': 'Diagnóstico no encontrado'}), 404
    
    # Obtener datos detallados
    diagnosis_dict = diagnosis.to_dict()
    
    # Agregar datos decodificados
    if diagnosis.google_maps_data:
        diagnosis_dict['google_maps_data'] = json.loads(diagnosis.google_maps_data)
    
    if diagnosis.website_data:
        diagnosis_dict['website_data'] = json.loads(diagnosis.website_data)
    
    if diagnosis.social_media_data:
        diagnosis_dict['social_media_data'] = json.loads(diagnosis.social_media_data)
    
    if diagnosis.inconsistencies:
        diagnosis_dict['inconsistencies'] = json.loads(diagnosis.inconsistencies)
    
    # Obtener información del negocio asociado
    business = Business.query.get(diagnosis.business_id)
    if business:
        diagnosis_dict['business'] = business.to_dict()
    
    return jsonify({'diagnosis': diagnosis_dict}), 200

@bp.route('', methods=['POST'])
@jwt_required()
def create_diagnosis():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validar datos requeridos
    if not data or not data.get('business_id'):
        return jsonify({'error': 'El ID del negocio es requerido'}), 400
    
    # Verificar que el negocio existe y pertenece al usuario
    business = Business.query.filter_by(id=data['business_id'], user_id=user_id).first()
    if not business:
        return jsonify({'error': 'Negocio no encontrado o no autorizado'}), 404
    
    # Verificar que el escaneo existe y pertenece al usuario (si se proporciona)
    if 'scan_id' in data and data['scan_id']:
        scan = Scan.query.filter_by(id=data['scan_id'], user_id=user_id).first()
        if not scan:
            return jsonify({'error': 'Escaneo no encontrado o no autorizado'}), 400
    
    # Validar puntuaciones si se proporcionan
    for score_field in ['google_maps_score', 'website_score', 'social_media_score', 'overall_score']:
        if score_field in data:
            try:
                score = int(data[score_field])
                if not (0 <= score <= 100):
                    return jsonify({'error': f'{score_field} debe estar entre 0 y 100'}), 400
            except (ValueError, TypeError):
                return jsonify({'error': f'{score_field} debe ser un número entero'}), 400
    
    # Crear nuevo diagnóstico
    try:
        diagnosis = Diagnosis(
            business_id=data['business_id'],
            scan_id=data.get('scan_id'),
            google_maps_score=data.get('google_maps_score'),
            website_score=data.get('website_score'),
            social_media_score=data.get('social_media_score'),
            overall_score=data.get('overall_score'),
            google_maps_data=json.dumps(data.get('google_maps_data', {})),
            website_data=json.dumps(data.get('website_data', {})),
            social_media_data=json.dumps(data.get('social_media_data', {})),
            inconsistencies=json.dumps(data.get('inconsistencies', [])),
            user_id=user_id
        )
        
        db.session.add(diagnosis)
        db.session.commit()
        
        return jsonify({
            'message': 'Diagnóstico creado exitosamente',
            'diagnosis': diagnosis.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al crear diagnóstico: {str(e)}'}), 500

@bp.route('/<diagnosis_id>', methods=['PUT'])
@jwt_required()
def update_diagnosis(diagnosis_id):
    user_id = get_jwt_identity()
    
    diagnosis = Diagnosis.query.filter_by(id=diagnosis_id, user_id=user_id).first()
    
    if not diagnosis:
        return jsonify({'error': 'Diagnóstico no encontrado'}), 404
    
    data = request.get_json()
    
    # Validar puntuaciones si se proporcionan
    for score_field in ['google_maps_score', 'website_score', 'social_media_score', 'overall_score']:
        if score_field in data:
            try:
                score = int(data[score_field])
                if not (0 <= score <= 100):
                    return jsonify({'error': f'{score_field} debe estar entre 0 y 100'}), 400
                setattr(diagnosis, score_field, score)
            except (ValueError, TypeError):
                return jsonify({'error': f'{score_field} debe ser un número entero'}), 400
    
    # Actualizar datos JSON si se proporcionan
    if 'google_maps_data' in data:
        diagnosis.google_maps_data = json.dumps(data['google_maps_data'])
    
    if 'website_data' in data:
        diagnosis.website_data = json.dumps(data['website_data'])
    
    if 'social_media_data' in data:
        diagnosis.social_media_data = json.dumps(data['social_media_data'])
    
    if 'inconsistencies' in data:
        diagnosis.inconsistencies = json.dumps(data['inconsistencies'])
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Diagnóstico actualizado exitosamente',
            'diagnosis': diagnosis.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar diagnóstico: {str(e)}'}), 500

@bp.route('/<diagnosis_id>', methods=['DELETE'])
@jwt_required()
def delete_diagnosis(diagnosis_id):
    user_id = get_jwt_identity()
    
    diagnosis = Diagnosis.query.filter_by(id=diagnosis_id, user_id=user_id).first()
    
    if not diagnosis:
        return jsonify({'error': 'Diagnóstico no encontrado'}), 404
    
    try:
        db.session.delete(diagnosis)
        db.session.commit()
        
        return jsonify({'message': 'Diagnóstico eliminado exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al eliminar diagnóstico: {str(e)}'}), 500

@bp.route('/business/<business_id>/latest', methods=['GET'])
@jwt_required()
def get_latest_diagnosis_for_business(business_id):
    user_id = get_jwt_identity()
    
    # Verificar que el negocio existe y pertenece al usuario
    business = Business.query.filter_by(id=business_id, user_id=user_id).first()
    if not business:
        return jsonify({'error': 'Negocio no encontrado o no autorizado'}), 404
    
    # Obtener el diagnóstico más reciente para este negocio
    diagnosis = Diagnosis.query.filter_by(business_id=business_id, user_id=user_id)\
                           .order_by(Diagnosis.created_at.desc())\
                           .first()
    
    if not diagnosis:
        return jsonify({'error': 'No se encontraron diagnósticos para este negocio'}), 404
    
    # Obtener datos detallados
    diagnosis_dict = diagnosis.to_dict()
    
    # Agregar datos decodificados
    if diagnosis.google_maps_data:
        diagnosis_dict['google_maps_data'] = json.loads(diagnosis.google_maps_data)
    
    if diagnosis.website_data:
        diagnosis_dict['website_data'] = json.loads(diagnosis.website_data)
    
    if diagnosis.social_media_data:
        diagnosis_dict['social_media_data'] = json.loads(diagnosis.social_media_data)
    
    if diagnosis.inconsistencies:
        diagnosis_dict['inconsistencies'] = json.loads(diagnosis.inconsistencies)
    
    # Agregar información del negocio
    diagnosis_dict['business'] = business.to_dict()
    
    return jsonify({'diagnosis': diagnosis_dict}), 200