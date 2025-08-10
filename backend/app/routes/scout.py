from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.models import ScoutScan, ScoutBusiness, ScoutDiagnostic
from app import db

scout_bp = Blueprint('scout', __name__)

@scout_bp.route('/scans', methods=['POST'])
@jwt_required()
def create_scan():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    # Validar datos requeridos
    required_fields = ['zone_name', 'latitude_north', 'latitude_south', 'longitude_east', 'longitude_west']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Field '{field}' is required"}), 400
    
    # Crear nuevo escaneo
    scan = ScoutScan(
        user_id=current_user_id,
        zone_name=data['zone_name'],
        latitude_north=data['latitude_north'],
        latitude_south=data['latitude_south'],
        longitude_east=data['longitude_east'],
        longitude_west=data['longitude_west'],
        category=data.get('category')
    )
    
    db.session.add(scan)
    db.session.commit()
    
    return jsonify(scan.to_dict()), 201

@scout_bp.route('/businesses', methods=['POST'])
@jwt_required()
def create_business():
    data = request.get_json()
    
    # Validar datos requeridos
    required_fields = ['scan_id', 'name', 'address', 'category', 'latitude', 'longitude']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Field '{field}' is required"}), 400
    
    # Crear nuevo negocio
    business = ScoutBusiness(
        scan_id=data['scan_id'],
        name=data['name'],
        address=data['address'],
        phone=data.get('phone'),
        website=data.get('website'),
        category=data['category'],
        latitude=data['latitude'],
        longitude=data['longitude'],
        google_maps_rating=data.get('google_maps_rating'),
        google_maps_reviews=data.get('google_maps_reviews'),
        website_exists=data.get('website_exists', False),
        facebook_page=data.get('facebook_page'),
        instagram_profile=data.get('instagram_profile'),
        twitter_profile=data.get('twitter_profile')
    )
    
    db.session.add(business)
    db.session.commit()
    
    return jsonify(business.to_dict()), 201

@scout_bp.route('/diagnostics', methods=['POST'])
@jwt_required()
def create_diagnostic():
    data = request.get_json()
    
    # Validar datos requeridos
    required_fields = ['business_id', 'digital_presence_score', 'google_maps_score', 
                      'website_score', 'social_media_score']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Field '{field}' is required"}), 400
    
    # Crear nuevo diagnóstico
    diagnostic = ScoutDiagnostic(
        business_id=data['business_id'],
        digital_presence_score=data['digital_presence_score'],
        google_maps_score=data['google_maps_score'],
        website_score=data['website_score'],
        social_media_score=data['social_media_score'],
        recommendations=data.get('recommendations')
    )
    
    db.session.add(diagnostic)
    db.session.commit()
    
    return jsonify(diagnostic.to_dict()), 201