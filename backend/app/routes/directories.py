from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.models import Dealership, Lead
from app import db

directories_bp = Blueprint('directories', __name__)

@directories_bp.route('/dealerships', methods=['GET'])
def get_dealerships():
    # Obtener parámetros de consulta
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category = request.args.get('category', type=str)
    
    # Construir consulta
    query = Dealership.query
    
    # Filtrar por categoría si se proporciona
    if category:
        query = query.filter_by(category=category)
    
    # Paginar resultados
    dealerships = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'dealerships': [dealership.to_dict() for dealership in dealerships.items],
        'total': dealerships.total,
        'pages': dealerships.pages,
        'current_page': dealerships.page
    })

@directories_bp.route('/dealerships', methods=['POST'])
#@jwt_required()
def create_dealership():
    data = request.get_json()
    
    # Validar datos requeridos
    required_fields = ['name', 'address', 'category']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Field '{field}' is required"}), 400
    
    # Crear nuevo concesionario
    dealership = Dealership(
        name=data['name'],
        address=data['address'],
        phone=data.get('phone'),
        email=data.get('email'),
        website=data.get('website'),
        brands=data.get('brands'),
        category=data['category'],
        latitude=data.get('latitude'),
        longitude=data.get('longitude')
    )
    
    db.session.add(dealership)
    db.session.commit()
    
    return jsonify(dealership.to_dict()), 201

@directories_bp.route('/leads', methods=['POST'])
def create_lead():
    data = request.get_json()
    
    # Validar datos requeridos
    required_fields = ['name', 'email']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Field '{field}' is required"}), 400
    
    # Crear nuevo lead
    lead = Lead(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        message=data.get('message'),
        dealership_id=data.get('dealership_id')
    )
    
    db.session.add(lead)
    db.session.commit()
    
    return jsonify(lead.to_dict()), 201