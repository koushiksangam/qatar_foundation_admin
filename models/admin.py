from datetime import datetime
from flask_login import UserMixin
from extensions import db

class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to enforce data ownership
    opportunities = db.relationship('Opportunity', backref='creator', lazy=True, cascade="all, delete-orphan")