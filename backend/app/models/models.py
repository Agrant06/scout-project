from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Dealership(db.Model):
    __tablename__ = 'dealerships'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(200), nullable=True)
    brands = db.Column(db.Text, nullable=True)  # JSON string
    category = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'website': self.website,
            'brands': self.brands,
            'category': self.category,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Lead(db.Model):
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    message = db.Column(db.Text, nullable=True)
    dealership_id = db.Column(db.Integer, db.ForeignKey('dealerships.id'), nullable=True)
    status = db.Column(db.String(20), default='new')  # new, contacted, qualified, closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    dealership = db.relationship('Dealership', backref=db.backref('leads', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'message': self.message,
            'dealership_id': self.dealership_id,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ScoutScan(db.Model):
    __tablename__ = 'scout_scans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    zone_name = db.Column(db.String(100), nullable=False)
    latitude_north = db.Column(db.Float, nullable=False)
    latitude_south = db.Column(db.Float, nullable=False)
    longitude_east = db.Column(db.Float, nullable=False)
    longitude_west = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('scout_scans', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'zone_name': self.zone_name,
            'latitude_north': self.latitude_north,
            'latitude_south': self.latitude_south,
            'longitude_east': self.longitude_east,
            'longitude_west': self.longitude_west,
            'category': self.category,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ScoutBusiness(db.Model):
    __tablename__ = 'scout_businesses'
    
    id = db.Column(db.Integer, primary_key=True)
    scan_id = db.Column(db.Integer, db.ForeignKey('scout_scans.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    website = db.Column(db.String(200), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    google_maps_rating = db.Column(db.Float, nullable=True)
    google_maps_reviews = db.Column(db.Integer, nullable=True)
    website_exists = db.Column(db.Boolean, default=False)
    facebook_page = db.Column(db.String(200), nullable=True)
    instagram_profile = db.Column(db.String(200), nullable=True)
    twitter_profile = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    scan = db.relationship('ScoutScan', backref=db.backref('businesses', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'scan_id': self.scan_id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'website': self.website,
            'category': self.category,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'google_maps_rating': self.google_maps_rating,
            'google_maps_reviews': self.google_maps_reviews,
            'website_exists': self.website_exists,
            'facebook_page': self.facebook_page,
            'instagram_profile': self.instagram_profile,
            'twitter_profile': self.twitter_profile,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ScoutDiagnostic(db.Model):
    __tablename__ = 'scout_diagnostics'
    
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('scout_businesses.id'), nullable=False)
    digital_presence_score = db.Column(db.Float, nullable=False)  # 0-100
    google_maps_score = db.Column(db.Float, nullable=False)  # 0-100
    website_score = db.Column(db.Float, nullable=False)  # 0-100
    social_media_score = db.Column(db.Float, nullable=False)  # 0-100
    recommendations = db.Column(db.Text, nullable=True)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    business = db.relationship('ScoutBusiness', backref=db.backref('diagnostics', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'business_id': self.business_id,
            'digital_presence_score': self.digital_presence_score,
            'google_maps_score': self.google_maps_score,
            'website_score': self.website_score,
            'social_media_score': self.social_media_score,
            'recommendations': self.recommendations,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }