from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.business import Business
import json

bp = Blueprint('business', __name__, url_prefix='/api/businesses')

@bp.route('', methods=['GET'])
@jwt_required()
def get_businesses():
    user_id = get_jwt_identity()
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    businesses = Business.query.filter_by(user_id=user_id).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'businesses': [business.to_dict() for business in businesses.items],
        'total': businesses.total,
        'pages': businesses.pages,
        'current_page': businesses.page
    }), 200

@bp.route('/', methods=['POST'])
@jwt_required()
def create_business():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    required_fields = ['name', 'category', 'address', 'city', 'state']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'El campo {field} es requerido'}), 400
    
    business = Business(
        name=data['name'],
        description=data.get('description', ''),
        category=data['category'],
        address=data['address'],
        city=data['city'],
        state=data['state'],
        postal_code=data.get('postal_code', ''),
        country=data.get('country', 'Argentina'),
        phone=data.get('phone', ''),
        email=data.get('email', ''),
        website=data.get('website', ''),
        latitude=float(data.get('latitude')) if 'latitude' in data else None,
        longitude=float(data.get('longitude')) if 'longitude' in data else None,
        google_places_id=data.get('google_places_id', ''),
        user_id=user_id
    )
    
    db.session.add(business)
    db.session.commit()
    
    return jsonify({
        'message': 'Comercio creado exitosamente',
        'business': business.to_dict()
    }), 201
