from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.diagnosis import Diagnosis
from app.models.business import Business
import json

bp = Blueprint('diagnosis', __name__, url_prefix='/api/diagnoses')

@bp.route('', methods=['GET'])
@jwt_required()
def get_diagnoses():
    user_id = get_jwt_identity()
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    business_id = request.args.get('business_id', None)
    
    query = Diagnosis.query.filter_by(user_id=user_id)
    
    if business_id:
        query = query.filter_by(business_id=business_id)
    
    diagnoses = query.order_by(Diagnosis.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'diagnoses': [diagnosis.to_dict() for diagnosis in diagnoses.items],
        'total': diagnoses.total,
        'pages': diagnoses.pages,
        'current_page': diagnoses.page
    }), 200

@bp.route('/', methods=['POST'])
@jwt_required()
def create_diagnosis():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('business_id'):
        return jsonify({'error': 'El ID del negocio es requerido'}), 400
    
    business = Business.query.filter_by(id=data['business_id'], user_id=user_id).first()
    if not business:
        return jsonify({'error': 'Negocio no encontrado o no autorizado'}), 400
    
    diagnosis = Diagnosis(
        business_id=data['business_id'],
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
