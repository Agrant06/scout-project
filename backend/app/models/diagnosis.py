from datetime import datetime
from app import db
import uuid

class Diagnosis(db.Model):
    __tablename__ = 'diagnoses'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = db.Column(db.String(36), db.ForeignKey('businesses.id'), nullable=False)
    scan_id = db.Column(db.String(36), db.ForeignKey('scans.id'), nullable=True)
    
    # Puntuaciones (0-100)
    google_maps_score = db.Column(db.Integer, nullable=True)
    website_score = db.Column(db.Integer, nullable=True)
    social_media_score = db.Column(db.Integer, nullable=True)
    overall_score = db.Column(db.Integer, nullable=True)
    
    # Datos del diagnóstico (JSON)
    google_maps_data = db.Column(db.Text, nullable=True)  # JSON con datos de Google Maps
    website_data = db.Column(db.Text, nullable=True)  # JSON con datos del sitio web
    social_media_data = db.Column(db.Text, nullable=True)  # JSON con datos de redes sociales
    inconsistencies = db.Column(db.Text, nullable=True)  # JSON con inconsistencias encontradas
    
    # Metadatos
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<Diagnosis {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'business_id': self.business_id,
            'scan_id': self.scan_id,
            'google_maps_score': self.google_maps_score,
            'website_score': self.website_score,
            'social_media_score': self.social_media_score,
            'overall_score': self.overall_score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'user_id': self.user_id
        }