import logging
from flask import Flask, jsonify, render_template
from config import Config
from extensions import db, login_manager, migrate
from models.admin import Admin
from routes import register_blueprints

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    register_blueprints(app)

    @app.route('/')
    def home():
        return render_template('admin.html')

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Admin, int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({
            "status": "error",
            "message": "Unauthorized. Please log in."
        }), 401

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            "status": "error",
            "message": "Resource not found"
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        app.logger.error(f"Server Error: {str(error)}")
        return jsonify({
            "status": "error",
            "message": "An internal server error occurred."
        }), 500

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.logger.info("Database initialized successfully.")
    app.run(debug=True, host='0.0.0.0', port=5000)