import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

class Config:
    """Base configuration with production-ready defaults."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_fallback_secret_key_change_in_prod')
    
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///qatar_admin.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session Security
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'