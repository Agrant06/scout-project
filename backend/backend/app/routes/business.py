from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.business import Business
from app.models.user import User
import json

bp = Blueprint('business', __name__, url_prefix='/api/businesses')

@bp.route('', methods=['GET'])
@jwt_required()
def get_businesses():
    user_id = get_jwt_identity()
    
    # Obtener parámetros de paginación y filtrado
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category = request.args.get('category', None)
    city = request.args.get('city', None)
    scan_id = request.args.get('scan_id', None)
    
    # Construir consulta
    query = Business.query.filter_by(user_id=user_id)
    
    if category:
        query = query.filter_by(category=category)
    
    if city:
        query = query.filter(Business.city.ilike(f'%{city}%'))
    
    if scan_id:
        # Aquí podrías agregar lógica para filtrar por escaneo
        # Por ahora, lo dejamos como placeholder
        pass
    
    # Ordenar por fecha de creación descendente
    query = query.order_by(Business.created_at.desc())
    
    # Paginar resultados
    businesses = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'businesses': [business.to_dict() for business in businesses.items],
        'total': businesses.total,
        'pages': businesses.pages,
        'current_page': businesses.page
    }), 200

@bp.route('/<business_id>', methods=['GET'])
@jwt_required()
def get_business(business_id):
    user_id = get_jwt_identity()
    
    business = Business.query.filter_by(id=business_id, user_id=user_id).first()
    
    if not business:
        return jsonify({'error': 'Comercio no encontrado'}), 404
    
    return jsonify({'business': business.to_dict()}), 200

@bp.route('', methods=['POST'])
@jwt_required()
def create_business():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validar datos requeridos
    required_fields = ['name', 'category', 'address', 'city', 'state']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'El campo {field} es requerido'}), 400
    
    # Validar coordenadas si se proporcionan
    if 'latitude' in data:
        try:
            latitude = float(data['latitude'])
            if not (-90 <= latitude <= 90):
                return jsonify({'error': 'Latitud debe estar entre -90 y 90'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Latitud debe ser un número válido'}), 400
    
    if 'longitude' in data:
        try:
            longitude = float(data['longitude'])
            if not (-180 <= longitude <= 180):
                return jsonify({'error': 'Longitud debe estar entre -180 y 180'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Longitud debe ser un número válido'}), 400
    
    # Crear nuevo comercio
    try:
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
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al crear comercio: {str(e)}'}), 500

@bp.route('/<business_id>', methods=['PUT'])
@jwt_required()
def update_business(business_id):
    user_id = get_jwt_identity()
    
    business = Business.query.filter_by(id=business_id, user_id=user_id).first()
    
    if not business:
        return jsonify({'error': 'Comercio no encontrado'}), 404
    
    data = request.get_json()
    
    # Actualizar campos permitidos
    if 'name' in data:
        business.name = data['name']
    if 'description' in data:
        business.description = data['description']
    if 'category' in data:
        business.category = data['category']
    if 'address' in data:
        business.address = data['address']
    if 'city' in data:
        business.city = data['city']
    if 'state' in data:
        business.state = data['state']
    if 'postal_code' in data:
        business.postal_code = data['postal_code']
    if 'country' in data:
        business.country = data['country']
    if 'phone' in data:
        business.phone = data['phone']
    if 'email' in data:
        business.email = data['email']
    if 'website' in data:
        business.website = data['website']
    
    # Validar y actualizar coordenadas
    if 'latitude' in data:
        try:
            business.latitude = float(data['latitude'])
            if not (-90 <= business.latitude <= 90):
                return jsonify({'error': 'Latitud debe estar entre -90 y 90'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Latitud debe ser un número válido'}), 400
    
    if 'longitude' in data:
        try:
            business.longitude = float(data['longitude'])
            if not (-180 <= business.longitude <= 180):
                return jsonify({'error': 'Longitud debe estar entre -180 y 180'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Longitud debe ser un número válido'}), 400
    
    if 'google_places_id' in data:
        business.google_places_id = data['google_places_id']
    
    if 'is_active' in data:
        business.is_active = bool(data['is_active'])
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Comercio actualizado exitosamente',
            'business': business.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar comercio: {str(e)}'}), 500

@bp.route('/<business_id>', methods=['DELETE'])
@jwt_required()
def delete_business(business_id):
    user_id = get_jwt_identity()
    
    business = Business.query.filter_by(id=business_id, user_id=user_id).first()
    
    if not business:
        return jsonify({'error': 'Comercio no encontrado'}), 404
    
    try:
        db.session.delete(business)
        db.session.commit()
        
        return jsonify({'message': 'Comercio eliminado exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al eliminar comercio: {str(e)}'}), 500

@bp.route('/search', methods=['GET'])
@jwt_required()
def search_businesses():
    user_id = get_jwt_identity()
    
    # Obtener parámetros de búsqueda
    query = request.args.get('q', '')
    latitude = request.args.get('lat', type=float)
    longitude = request.args.get('lng', type=float)
    radius = request.args.get('radius', type=float, default=5000)  # 5km por defecto
    category = request.args.get('category', None)
    
    # Construir consulta base
    from sqlalchemy import or_, and_
    business_query = Business.query.filter_by(user_id=user_id)
    
    # Aplicar filtro de texto si se proporciona
    if query:
        business_query = business_query.filter(
            or_(
                Business.name.ilike(f'%{query}%'),
                Business.description.ilike(f'%{query}%'),
                Business.category.ilike(f'%{query}%'),
                Business.address.ilike(f'%{query}%'),
                Business.city.ilike(f'%{query}%')
            )
        )
    
    # Aplicar filtro de categoría si se proporciona
    if category:
        business_query = business_query.filter(Business.category.ilike(f'%{category}%'))
    
    # Aplicar filtro geográfico si se proporcionan coordenadas
    if latitude is not None and longitude is not None and radius is not None:
        # Fórmula de Haversine para calcular distancia
        # Esta es una simplificación, en producción deberías usar funciones geoespaciales de PostgreSQL
        business_query = business_query.filter(
            and_(
                Business.latitude.isnot(None),
                Business.longitude.isnot(None)
            )
        )
        # La filtración por distancia se debería hacer a nivel de base de datos con funciones geoespaciales
        # Por ahora, traeremos todos y filtraremos en código
    
    # Ejecutar consulta
    businesses = business_query.all()
    
    # Filtrar por distancia si se proporcionaron coordenadas
    if latitude is not None and longitude is not None and radius is not None:
        from math import radians, cos, sin, asin, sqrt
        
        def haversine(lat1, lon1, lat2, lon2):
            # Convertir grados a radianes
            lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
            
            # Fórmula de Haversine
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a))
            
            # Radio de la Tierra en metros
            r = 6371000
            return c * r
        
        filtered_businesses = []
        for business in businesses:
            if business.latitude and business.longitude:
                distance = haversine(latitude, longitude, business.latitude, business.longitude)
                if distance <= radius:
                    business_dict = business.to_dict()
                    business_dict['distance'] = round(distance, 2)
                    filtered_businesses.append(business_dict)
        
        # Ordenar por distancia
        filtered_businesses.sort(key=lambda x: x['distance'])
        
        return jsonify({
            'businesses': filtered_businesses,
            'total': len(filtered_businesses)
        }), 200
    
    return jsonify({
        'businesses': [business.to_dict() for business in businesses],
        'total': len(businesses)
    }), 200