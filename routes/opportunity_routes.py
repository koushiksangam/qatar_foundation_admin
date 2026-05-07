from flask import Blueprint, request
from flask_login import login_required, current_user
from utils.helpers import get_request_data
from utils.responses import handle_service_result
from services.opportunity_service import (
    get_opportunities_by_admin,
    create_opportunity,
    get_opportunity,
    update_opportunity,
    delete_opportunity
)

opp_bp = Blueprint('opportunities', __name__, url_prefix='/api/opportunities')

@opp_bp.route('', methods=['GET'])
@login_required
def get_all():
    result = get_opportunities_by_admin(current_user.id)
    return handle_service_result(result)

@opp_bp.route('', methods=['POST'])
@login_required
def create():
    data = get_request_data(request)
    result = create_opportunity(current_user.id, data)
    return handle_service_result(result)

@opp_bp.route('/<int:opp_id>', methods=['GET'])
@login_required
def get_single(opp_id):
    result = get_opportunity(current_user.id, opp_id)
    return handle_service_result(result)

@opp_bp.route('/<int:opp_id>', methods=['PUT'])
@login_required
def update(opp_id):
    data = get_request_data(request)
    result = update_opportunity(current_user.id, opp_id, data)
    return handle_service_result(result)

@opp_bp.route('/<int:opp_id>', methods=['DELETE'])
@login_required
def delete_opportunity_route(opp_id):
    result = delete_opportunity(current_user.id, opp_id)
    return handle_service_result(result)