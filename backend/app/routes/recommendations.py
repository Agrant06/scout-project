from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.recommendation import Recommendation
from app.models.diagnosis import Diagnosis
from app.models.user import User
from datetime import datetime

bp = Blueprint('recommendations', __name__, url_prefix='/api/recommendations')

@bp.route('', methods=['GET'])
@jwt_required()
def get_recommendations():
    user_id = get_jwt_identity()
    
    # Obtener parámetros de paginación y filtrado
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    diagnosis_id = request.args.get('diagnosis_id', None)
    category = request.args.get('category', None)
    priority = request.args.get('priority', None)
    status = request.args.get('status', None)
    
    # Construir consulta
    query = Recommendation.query.filter_by(user_id=user_id)
    
    if diagnosis_id:
        query = query.filter_by(diagnosis_id=diagnosis_id)
    
    if category:
        query = query.filter_by(category=category)
    
    if priority:
        query = query.filter_by(priority=priority)
    
    if status:
        query = query.filter_by(status=status)
    
    # Ordenar por prioridad y fecha de creación
    priority_order = {
        'critical': 1,
        'high': 2,
        'medium': 3,
        'low': 4
    }
    
    # Ordenar por prioridad (críticas primero) y luego por fecha de creación
    recommendations = query.all()
    recommendations.sort(key=lambda r: (
        priority_order.get(r.priority, 5),
        r.created_at
    ))
    
    # Paginar manualmente
    start = (page - 1) * per_page
    end = start + per_page
    paginated_recommendations = recommendations[start:end]
    
    return jsonify({
        'recommendations': [rec.to_dict() for rec in paginated_recommendations],
        'total': len(recommendations),
        'pages': (len(recommendations) + per_page - 1) // per_page,
        'current_page': page
    }), 200

@bp.route('/<recommendation_id>', methods=['GET'])
@jwt_required()
def get_recommendation(recommendation_id):
    user_id = get_jwt_identity()
    
    recommendation = Recommendation.query.filter_by(id=recommendation_id, user_id=user_id).first()
    
    if not recommendation:
        return jsonify({'error': 'Recomendación no encontrada'}), 404
    
    # Obtener información del diagnóstico asociado
    diagnosis_dict = None
    diagnosis = Diagnosis.query.get(recommendation.diagnosis_id)
    if diagnosis:
        diagnosis_dict = diagnosis.to_dict()
    
    return jsonify({
        'recommendation': recommendation.to_dict(),
        'diagnosis': diagnosis_dict
    }), 200

@bp.route('', methods=['POST'])
@jwt_required()
def create_recommendation():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validar datos requeridos
    required_fields = ['diagnosis_id', 'title', 'description', 'category']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'El campo {field} es requerido'}), 400
    
    # Verificar que el diagnóstico existe y pertenece al usuario
    diagnosis = Diagnosis.query.filter_by(id=data['diagnosis_id'], user_id=user_id).first()
    if not diagnosis:
        return jsonify({'error': 'Diagnóstico no encontrado o no autorizado'}), 400
    
    # Validar categoría
    valid_categories = ['google_maps', 'website', 'social_media', 'general']
    if data['category'] not in valid_categories:
        return jsonify({'error': f'Categoría inválida. Debe ser una de: {", ".join(valid_categories)}'}), 400
    
    # Validar prioridad
    valid_priorities = ['low', 'medium', 'high', 'critical']
    if 'priority' in data and data['priority'] not in valid_priorities:
        return jsonify({'error': f'Prioridad inválida. Debe ser una de: {", ".join(valid_priorities)}'}), 400
    
    # Validar dificultad
    valid_difficulties = ['easy', 'medium', 'hard', 'expert']
    if 'difficulty' in data and data['difficulty'] not in valid_difficulties:
        return jsonify({'error': f'Dificultad inválida. Debe ser una de: {", ".join(valid_difficulties)}'}), 400
    
    # Validar estado
    valid_statuses = ['pending', 'in_progress', 'completed', 'dismissed']
    if 'status' in data and data['status'] not in valid_statuses:
        return jsonify({'error': f'Estado inválido. Debe ser uno de: {", ".join(valid_statuses)}'}), 400
    
    # Crear nueva recomendación
    try:
        recommendation = Recommendation(
            diagnosis_id=data['diagnosis_id'],
            title=data['title'],
            description=data['description'],
            category=data['category'],
            priority=data.get('priority', 'medium'),
            difficulty=data.get('difficulty', 'medium'),
            estimated_time=data.get('estimated_time', ''),
            status=data.get('status', 'pending'),
            implementation_notes=data.get('implementation_notes', ''),
            user_id=user_id
        )
        
        db.session.add(recommendation)
        db.session.commit()
        
        return jsonify({
            'message': 'Recomendación creada exitosamente',
            'recommendation': recommendation.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al crear recomendación: {str(e)}'}), 500

@bp.route('/<recommendation_id>', methods=['PUT'])
@jwt_required()
def update_recommendation(recommendation_id):
    user_id = get_jwt_identity()
    
    recommendation = Recommendation.query.filter_by(id=recommendation_id, user_id=user_id).first()
    
    if not recommendation:
        return jsonify({'error': 'Recomendación no encontrada'}), 404
    
    data = request.get_json()
    
    # Actualizar campos permitidos
    if 'title' in data:
        recommendation.title = data['title']
    
    if 'description' in data:
        recommendation.description = data['description']
    
    if 'category' in data:
        valid_categories = ['google_maps', 'website', 'social_media', 'general']
        if data['category'] not in valid_categories:
            return jsonify({'error': f'Categoría inválida. Debe ser una de: {", ".join(valid_categories)}'}), 400
        recommendation.category = data['category']
    
    if 'priority' in data:
        valid_priorities = ['low', 'medium', 'high', 'critical']
        if data['priority'] not in valid_priorities:
            return jsonify({'error': f'Prioridad inválida. Debe ser una de: {", ".join(valid_priorities)}'}), 400
        recommendation.priority = data['priority']
    
    if 'difficulty' in data:
        valid_difficulties = ['easy', 'medium', 'hard', 'expert']
        if data['difficulty'] not in valid_difficulties:
            return jsonify({'error': f'Dificultad inválida. Debe ser una de: {", ".join(valid_difficulties)}'}), 400
        recommendation.difficulty = data['difficulty']
    
    if 'estimated_time' in data:
        recommendation.estimated_time = data['estimated_time']
    
    if 'status' in data:
        valid_statuses = ['pending', 'in_progress', 'completed', 'dismissed']
        if data['status'] not in valid_statuses:
            return jsonify({'error': f'Estado inválido. Debe ser uno de: {", ".join(valid_statuses)}'}), 400
        recommendation.status = data['status']
        
        # Si se marca como completada, registrar la fecha
        if data['status'] == 'completed' and recommendation.completed_at is None:
            recommendation.completed_at = datetime.utcnow()
    
    if 'implementation_notes' in data:
        recommendation.implementation_notes = data['implementation_notes']
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Recomendación actualizada exitosamente',
            'recommendation': recommendation.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar recomendación: {str(e)}'}), 500

@bp.route('/<recommendation_id>', methods=['DELETE'])
@jwt_required()
def delete_recommendation(recommendation_id):
    user_id = get_jwt_identity()
    
    recommendation = Recommendation.query.filter_by(id=recommendation_id, user_id=user_id).first()
    
    if not recommendation:
        return jsonify({'error': 'Recomendación no encontrada'}), 404
    
    try:
        db.session.delete(recommendation)
        db.session.commit()
        
        return jsonify({'message': 'Recomendación eliminada exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al eliminar recomendación: {str(e)}'}), 500

@bp.route('/diagnosis/<diagnosis_id>', methods=['GET'])
@jwt_required()
def get_recommendations_for_diagnosis(diagnosis_id):
    user_id = get_jwt_identity()
    
    # Verificar que el diagnóstico existe y pertenece al usuario
    diagnosis = Diagnosis.query.filter_by(id=diagnosis_id, user_id=user_id).first()
    if not diagnosis:
        return jsonify({'error': 'Diagnóstico no encontrado o no autorizado'}), 404
    
    # Obtener todas las recomendaciones para este diagnóstico
    recommendations = Recommendation.query.filter_by(diagnosis_id=diagnosis_id, user_id=user_id).all()
    
    # Ordenar por prioridad
    priority_order = {
        'critical': 1,
        'high': 2,
        'medium': 3,
        'low': 4
    }
    
    recommendations.sort(key=lambda r: (
        priority_order.get(r.priority, 5),
        r.created_at
    ))
    
    return jsonify({
        'recommendations': [rec.to_dict() for rec in recommendations],
        'total': len(recommendations)
    }), 200

@bp.route('/<recommendation_id>/status', methods=['PUT'])
@jwt_required()
def update_recommendation_status(recommendation_id):
    user_id = get_jwt_identity()
    
    recommendation = Recommendation.query.filter_by(id=recommendation_id, user_id=user_id).first()
    
    if not recommendation:
        return jsonify({'error': 'Recomendación no encontrada'}), 404
    
    data = request.get_json()
    
    if not data or 'status' not in data:
        return jsonify({'error': 'El campo status es requerido'}), 400
    
    # Validar estado
    valid_statuses = ['pending', 'in_progress', 'completed', 'dismissed']
    if data['status'] not in valid_statuses:
        return jsonify({'error': f'Estado inválido. Debe ser uno de: {", ".join(valid_statuses)}'}), 400
    
    # Actualizar estado
    recommendation.status = data['status']
    
    # Si se marca como completada, registrar la fecha
    if data['status'] == 'completed' and recommendation.completed_at is None:
        recommendation.completed_at = datetime.utcnow()
    
    # Si se marca como en progreso y tenía fecha de completado, eliminarla
    if data['status'] == 'in_progress' and recommendation.completed_at is not None:
        recommendation.completed_at = None
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Estado de recomendación actualizado exitosamente',
            'recommendation': recommendation.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar estado de recomendación: {str(e)}'}), 500