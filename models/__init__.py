from .admin import Admin
from .opportunity import Opportunity

# Expose models for easy importing and Alembic migrations
__all__ = ['Admin', 'Opportunity']