from .auth_routes import auth_bp
from .opportunity_routes import opp_bp

def register_blueprints(app):
    """Registers all application routing blueprints cleanly."""
    app.register_blueprint(auth_bp)
    app.register_blueprint(opp_bp)