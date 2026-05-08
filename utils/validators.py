import re
from typing import List

VALID_CATEGORIES = {'technology', 'business', 'design', 'marketing', 'data', 'other'}
EMAIL_REGEX = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')

def validate_email(email: str) -> bool:
    if not email:
        return False
    return bool(EMAIL_REGEX.match(email))

def validate_password(password: str) -> bool:
    return bool(password and len(password) >= 8)

def validate_category(category: str) -> bool:
    return category in VALID_CATEGORIES

def get_missing_fields(data: dict, required_fields: List[str]) -> List[str]:
    """Returns a list of fields that are either missing or falsy."""
    return [field for field in required_fields if not data.get(field)]