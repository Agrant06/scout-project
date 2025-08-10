from datetime import datetime
from app import db
import uuid

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    diagnosis_id = db.Column(db.String(36), db.ForeignKey('diagnoses.id'), nullable=False)
    
    # Datos de la recomendación
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # google_maps, website, social_media, general
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    difficulty = db.Column(db.String(20), default='medium')  # easy, medium, hard, expert
    estimated_time = db.Column(db.String(50), nullable=True)  # Tiempo estimado para implementar
    
    # Datos de implementación
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed, dismissed
    implementation_notes = db.Column(db.Text, nullable=True)
    
    # Metadatos
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Relaciones
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<Recommendation {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'diagnosis_id': self.diagnosis_id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'priority': self.priority,
            'difficulty': self.difficulty,
            'estimated_time': self.estimated_time,
            'status': self.status,
            'implementation_notes': self.implementation_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'user_id': self.user_id
        }