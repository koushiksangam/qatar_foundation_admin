from flask import Blueprint, request, session
from flask_login import login_required, logout_user
from utils.helpers import get_request_data, ServiceResult
from utils.responses import handle_service_result
from services.auth_service import (
    register_admin,
    authenticate_admin,
    initiate_password_reset,
    finalize_password_reset
)

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = get_request_data(request)
    result = register_admin(data)
    return handle_service_result(result)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = get_request_data(request)
    result = authenticate_admin(data)

    if result.success and result.extra.get('_remember_me'):
        session.permanent = True

    return handle_service_result(result)

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    result = ServiceResult(
        success=True,
        message='Logged out successfully',
        extra={"redirect": "/"}
    )
    return handle_service_result(result)

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = get_request_data(request)
    result = initiate_password_reset(data)
    return handle_service_result(result)

@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    data = get_request_data(request)
    result = finalize_password_reset(token, data)
    return handle_service_result(result)