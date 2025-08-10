from datetime import datetime
from app import db
import uuid

class Scan(db.Model):
    __tablename__ = 'scans'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    center_latitude = db.Column(db.Float, nullable=False)
    center_longitude = db.Column(db.Float, nullable=False)
    radius = db.Column(db.Float, nullable=False)  # Radio en metros
    categories = db.Column(db.Text, nullable=True)  # JSON con categorías seleccionadas
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Relaciones
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f'<Scan {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'center_latitude': self.center_latitude,
            'center_longitude': self.center_longitude,
            'radius': self.radius,
            'categories': self.categories,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'user_id': self.user_id
        }