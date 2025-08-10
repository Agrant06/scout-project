from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.business import Business
from app.models.diagnosis import Diagnosis
from app.services.diagnosis_service import DiagnosisService
from datetime import datetime

bp = Blueprint('diagnosis_api', __name__, url_prefix='/api/diagnosis')

@bp.route('/business/<business_id>', methods=['POST'])
@jwt_required()
def create_business_diagnosis(business_id):
    """Crear un diagnóstico para un negocio específico"""
    user_id = get_jwt_identity()
    
    # Verificar que el negocio existe y pertenece al usuario
    business = Business.query.filter_by(id=business_id, user_id=user_id).first()
    if not business:
        return jsonify({'error': 'Negocio no encontrado o no autorizado'}), 404
    
    # Crear diagnóstico
    diagnosis_service = DiagnosisService()
    result = diagnosis_service.create_diagnosis(business_id, user_id)
    
    if result['status'] == 'success':
        return jsonify({
            'message': 'Diagnóstico creado exitosamente',
            'diagnosis_id': result['diagnosis_id'],
            'scores': result['scores'],
            'inconsistencies_count': result['inconsistencies_count'],
            'recommendations_count': result['recommendations_count']
        }), 201
    else:
        return jsonify({'error': result['error']}), 500

@bp.route('/batch', methods=['POST'])
@jwt_required()
def batch_diagnosis():
    """Realizar diagnóstico por lotes para múltiples negocios"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or 'business_ids' not in data:
        return jsonify({'error': 'Se requiere la lista de IDs de negocios'}), 400
    
    business_ids = data['business_ids']
    if not isinstance(business_ids, list) or not business_ids:
        return jsonify({'error': 'business_ids debe ser una lista no vacía'}), 400
    
    # Verificar que todos los negocios existan y pertenezcan al usuario
    businesses = Business.query.filter(
        Business.id.in_(business_ids),
        Business.user_id == user_id
    ).all()
    
    valid_business_ids = [business.id for business in businesses]
    
    if len(valid_business_ids) != len(business_ids):
        return jsonify({
            'error': 'Algunos negocios no existen o no pertenecen al usuario'
        }), 400
    
    # Realizar diagnóstico por lotes
    diagnosis_service = DiagnosisService()
    results = diagnosis_service.batch_diagnosis(valid_business_ids, user_id)
    
    return jsonify({
        'message': 'Diagnóstico por lotes completado',
        'total': results['total'],
        'successful': len(results['successful']),
        'failed': len(results['failed']),
        'results': results
    }), 200

@bp.route('/<diagnosis_id>', methods=['GET'])
@jwt_required()
def get_diagnosis(diagnosis_id):
    """Obtener detalles de un diagnóstico específico"""
    user_id = get_jwt_identity()
    
    diagnosis = Diagnosis.query.filter_by(id=diagnosis_id, user_id=user_id).first()
    if not diagnosis:
        return jsonify({'error': 'Diagnóstico no encontrado'}), 404
    
    # Obtener información del negocio
    business = Business.query.get(diagnosis.business_id)
    
    # Construir respuesta
    response = {
        'diagnosis': {
            'id': diagnosis.id,
            'business_id': diagnosis.business_id,
            'google_maps_score': diagnosis.google_maps_score,
            'website_score': diagnosis.website_score,
            'overall_score': diagnosis.overall_score,
            'created_at': diagnosis.created_at.isoformat() if diagnosis.created_at else None,
            'updated_at': diagnosis.updated_at.isoformat() if diagnosis.updated_at else None
        },
        'business': business.to_dict() if business else None
    }
    
    # Agregar datos decodificados si existen
    if diagnosis.google_maps_data:
        import json
        response['google_maps_data'] = json.loads(diagnosis.google_maps_data)
    
    if diagnosis.website_data:
        import json
        response['website_data'] = json.loads(diagnosis.website_data)
    
    if diagnosis.inconsistencies:
        import json
        response['inconsistencies'] = json.loads(diagnosis.inconsistencies)
    
    return jsonify(response), 200

@bp.route('/business/<business_id>/latest', methods=['GET'])
@jwt_required()
def get_latest_diagnosis(business_id):
    """Obtener el diagnóstico más reciente para un negocio"""
    user_id = get_jwt_identity()
    
    # Verificar que el negocio existe y pertenece al usuario
    business = Business.query.filter_by(id=business_id, user_id=user_id).first()
    if not business:
        return jsonify({'error': 'Negocio no encontrado o no autorizado'}), 404
    
    # Obtener diagnóstico más reciente
    diagnosis = Diagnosis.query.filter_by(business_id=business_id, user_id=user_id)\
                         .order_by(Diagnosis.created_at.desc())\
                         .first()
    
    if not diagnosis:
        return jsonify({'error': 'No se encontraron diagnósticos para este negocio'}), 404
    
    # Construir respuesta
    response = {
        'diagnosis': {
            'id': diagnosis.id,
            'business_id': diagnosis.business_id,
            'google_maps_score': diagnosis.google_maps_score,
            'website_score': diagnosis.website_score,
            'overall_score': diagnosis.overall_score,
            'created_at': diagnosis.created_at.isoformat() if diagnosis.created_at else None,
            'updated_at': diagnosis.updated_at.isoformat() if diagnosis.updated_at else None
        },
        'business': business.to_dict()
    }
    
    # Agregar datos decodificados si existen
    if diagnosis.google_maps_data:
        import json
        response['google_maps_data'] = json.loads(diagnosis.google_maps_data)
    
    if diagnosis.website_data:
        import json
        response['website_data'] = json.loads(diagnosis.website_data)
    
    if diagnosis.inconsistencies:
        import json
        response['inconsistencies'] = json.loads(diagnosis.inconsistencies)
    
    return jsonify(response), 200