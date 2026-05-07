import logging
from flask import url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_login import login_user

from extensions import db
from models.admin import Admin
from utils.helpers import ServiceResult
from utils.validators import validate_email, validate_password, get_missing_fields

logger = logging.getLogger(__name__)

def register_admin(data: dict) -> ServiceResult:
    """Handles business logic for US-1.1: Admin Sign Up."""
    required_fields = ['full_name', 'email', 'password', 'confirm_password']
    
    if missing := get_missing_fields(data, required_fields):
        return ServiceResult(False, f"Missing required fields: {', '.join(missing)}", status_code=400)
        
    email = data['email']
    password = data['password']
    
    if not validate_email(email):
        return ServiceResult(False, "Invalid email format.", status_code=400)
        
    if not validate_password(password):
        return ServiceResult(False, "Password must be at least 8 characters long.", status_code=400)
        
    if password != data['confirm_password']:
        return ServiceResult(False, "Passwords do not match.", status_code=400)
        
    if Admin.query.filter_by(email=email).first():
        return ServiceResult(False, "An account with this email already exists.", status_code=409)
        
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256:600000')
    admin = Admin(full_name=data['full_name'], email=email, password_hash=hashed_password)
    
    try:
        db.session.add(admin)
        db.session.commit()
        return ServiceResult(True, "Account created successfully. Redirecting to login...", 
                             status_code=201, extra={"redirect": "/login"})
    except Exception as e:
        db.session.rollback()
        logger.error(f"Signup error: {str(e)}")
        return ServiceResult(False, "An internal database error occurred.", status_code=500)

def authenticate_admin(data: dict) -> ServiceResult:
    """Handles business logic for US-1.2: Admin Login."""
    email = data.get('email')
    password = data.get('password')
    remember_me = str(data.get('remember_me', 'false')).lower() == 'true'
    
    if not email or not password:
        return ServiceResult(False, "Email and password are required.", status_code=400)
        
    admin = Admin.query.filter_by(email=email).first()
    
    if not admin or not check_password_hash(admin.password_hash, password):
        return ServiceResult(False, "Invalid email or password", status_code=401)
        
    login_user(admin, remember=remember_me)
    
    return ServiceResult(
        success=True, 
        message="Login successful", 
        status_code=200, 
        extra={"redirect": "/dashboard", "_remember_me": remember_me} # Private flag handled by route
    )

def initiate_password_reset(data: dict) -> ServiceResult:
    """Handles business logic for US-1.3: Forgot Password."""
    email = data.get('email')
    if not email:
        return ServiceResult(False, "Email is required.", status_code=400)
        
    admin = Admin.query.filter_by(email=email).first()
    success_msg = "If the email is registered, a password reset link has been sent."
    
    if admin:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = serializer.dumps(email, salt='password-reset-salt')
        reset_link = url_for('auth.reset_password_route', token=token, _external=True)
        
        logger.info(f"\n--- PASSWORD RESET LINK (Expires in 1 hour) ---\n"
                    f"Email: {email}\nLink: {reset_link}\n"
                    f"--------------------------------------------")
                    
    return ServiceResult(True, success_msg, status_code=200)

def finalize_password_reset(token: str, data: dict) -> ServiceResult:
    """Handles logic for updating the password post-token verification."""
    try:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except SignatureExpired:
        return ServiceResult(False, "The password reset link has expired.", status_code=400)
    except BadSignature:
        return ServiceResult(False, "Invalid password reset link.", status_code=400)
        
    new_password = data.get('password')
    if not validate_password(new_password):
        return ServiceResult(False, "Password must be at least 8 characters long.", status_code=400)
        
    admin = Admin.query.filter_by(email=email).first()
    if not admin:
        return ServiceResult(False, "User not found.", status_code=404)
        
    admin.password_hash = generate_password_hash(new_password, method='pbkdf2:sha256:600000')
    db.session.commit()
    
    return ServiceResult(True, "Password has been updated successfully. Please log in.", status_code=200)