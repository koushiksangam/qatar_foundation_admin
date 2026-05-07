from datetime import datetime
from extensions import db

class Opportunity(db.Model):
    __tablename__ = 'opportunities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    skills = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)
    future_opportunities = db.Column(db.String(255), nullable=False)
    max_applicants = db.Column(db.Integer, nullable=True)
    
    # Foreign key establishing strict ownership
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False, index=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self) -> dict:
        """Serializes the model to a dictionary compatible with the frontend JSON structure."""
        return {
            "id": self.id,
            "name": self.name,
            "duration": self.duration,
            "start_date": self.start_date,
            "description": self.description,
            "skills": self.skills.split(',') if self.skills else [],
            "category": self.category,
            "future_opportunities": self.future_opportunities,
            "max_applicants": self.max_applicants,
            "admin_id": self.admin_id
        }