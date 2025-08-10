from datetime import datetime
from app import db
import uuid

class Business(db.Model):
    __tablename__ = 'businesses'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(50), default='Argentina')
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    google_places_id = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relaciones
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    
    def __repr__(self):
        return f'<Business {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'postal_code': self.postal_code,
            'country': self.country,
            'phone': self.phone,
            'email': self.email,
            'website': self.website,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'google_places_id': self.google_places_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }