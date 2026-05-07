from dataclasses import dataclass, field
from typing import Any, Dict, Optional

@dataclass
class ServiceResult:
    """
    Standardized payload for communication between Services and Routes.
    Decouples HTTP semantics from business logic.
    """
    success: bool
    message: str
    data: Optional[Any] = None
    status_code: int = 200
    extra: Dict[str, Any] = field(default_factory=dict)

def get_request_data(request) -> dict:
    """Safely extracts data regardless of content type (JSON vs Form)."""
    if request.is_json:
        return request.get_json(silent=True) or {}
    return request.form.to_dict() or {}