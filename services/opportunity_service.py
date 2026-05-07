import logging
from extensions import db
from models.opportunity import Opportunity
from utils.helpers import ServiceResult
from utils.validators import validate_category, get_missing_fields

logger = logging.getLogger(__name__)

def get_opportunities_by_admin(admin_id: int) -> ServiceResult:
    """Fetches all opportunities mapped strictly to the active user session."""
    opps = Opportunity.query.filter_by(admin_id=admin_id).all()
    
    if not opps:
        return ServiceResult(True, "No opportunities found.", data=[], status_code=200)
        
    return ServiceResult(True, "Opportunities retrieved successfully.", 
                         data=[o.to_dict() for o in opps], status_code=200)

def create_opportunity(admin_id: int, data: dict) -> ServiceResult:
    """Creates a new opportunity and assigns explicit ownership."""
    required_fields = ['name', 'duration', 'start_date', 'description', 'skills', 'category', 'future_opportunities']
    
    if missing := get_missing_fields(data, required_fields):
        return ServiceResult(False, f"Missing required fields: {', '.join(missing)}", status_code=400)
        
    if not validate_category(data.get('category')):
        return ServiceResult(False, "Invalid category selected.", status_code=400)
        
    skills = data.get('skills')
    skills_str = ",".join(skills) if isinstance(skills, list) else str(skills)
    
    max_applicants = data.get('max_applicants')
    try:
        max_applicants = int(max_applicants) if max_applicants else None
    except ValueError:
        return ServiceResult(False, "Maximum applicants must be a valid integer.", status_code=400)
        
    opp = Opportunity(
        name=data['name'],
        duration=data['duration'],
        start_date=data['start_date'],
        description=data['description'],
        skills=skills_str,
        category=data['category'],
        future_opportunities=data['future_opportunities'],
        max_applicants=max_applicants,
        admin_id=admin_id
    )
    
    try:
        db.session.add(opp)
        db.session.commit()
        return ServiceResult(True, "Opportunity created successfully.", data=opp.to_dict(), status_code=201)
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to create opportunity: {str(e)}")
        return ServiceResult(False, "An internal error occurred while saving the opportunity.", status_code=500)

def get_opportunity(admin_id: int, opp_id: int) -> ServiceResult:
    """Fetches details for a single opportunity, validating ownership."""
    opp = Opportunity.query.filter_by(id=opp_id, admin_id=admin_id).first()
    
    if not opp:
        return ServiceResult(False, "Opportunity not found or access denied.", status_code=404)
        
    return ServiceResult(True, "Opportunity details retrieved.", data=opp.to_dict(), status_code=200)

def update_opportunity(admin_id: int, opp_id: int, data: dict) -> ServiceResult:
    """Safely updates an opportunity owned by the active admin."""
    opp = Opportunity.query.filter_by(id=opp_id, admin_id=admin_id).first()
    if not opp:
        return ServiceResult(False, "Opportunity not found or access denied.", status_code=404)
        
    if 'category' in data and not validate_category(data['category']):
        return ServiceResult(False, "Invalid category selected.", status_code=400)
        
    if 'max_applicants' in data:
        try:
            val = data['max_applicants']
            opp.max_applicants = int(val) if val else None
        except ValueError:
            return ServiceResult(False, "Maximum applicants must be a valid number.", status_code=400)
            
    updateable_fields = ['name', 'duration', 'start_date', 'description', 'future_opportunities']
    for field in updateable_fields:
        if field in data:
            val = data[field]
            if not val:
                return ServiceResult(False, f"{field.replace('_', ' ').title()} cannot be empty.", status_code=400)
            setattr(opp, field, val)
            
    if 'category' in data:
        opp.category = data['category']
        
    if 'skills' in data:
        skills = data['skills']
        if not skills:
            return ServiceResult(False, "Skills cannot be empty.", status_code=400)
        opp.skills = ",".join(skills) if isinstance(skills, list) else str(skills)
        
    try:
        db.session.commit()
        return ServiceResult(True, "Opportunity updated successfully.", data=opp.to_dict(), status_code=200)
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to update opportunity: {str(e)}")
        return ServiceResult(False, "An error occurred during update.", status_code=500)

def delete_opportunity(admin_id: int, opp_id: int) -> ServiceResult:
    """Permanently removes an opportunity, ensuring correct ownership."""
    opp = Opportunity.query.filter_by(id=opp_id, admin_id=admin_id).first()
    
    if not opp:
        return ServiceResult(False, "Opportunity not found or access denied.", status_code=404)
        
    try:
        db.session.delete(opp)
        db.session.commit()
        return ServiceResult(True, "Opportunity deleted successfully.", status_code=200)
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to delete opportunity: {str(e)}")
        return ServiceResult(False, "An error occurred during deletion.", status_code=500)