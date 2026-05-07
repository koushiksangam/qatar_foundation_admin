from flask import jsonify

def handle_service_result(result):
    """
    Translates a ServiceResult dataclass into a standardized Flask JSON response.
    Ensures absolute consistency across all API endpoints.
    """
    response = {
        "status": "success" if result.success else "error",
        "message": result.message
    }
    
    if result.data is not None:
        response["data"] = result.data
        
    # Inject any extra properties expected by the frontend (e.g., 'redirect')
    if result.extra:
        response.update(result.extra)
        
    return jsonify(response), result.status_code