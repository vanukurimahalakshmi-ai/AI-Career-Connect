import os
from flask import Flask
from app.config import Config
from app.models import db
from app.services.database_service import DatabaseService

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'] / 'audio', exist_ok=True)
    os.makedirs(app.root_path + '/../instance', exist_ok=True)

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    from app.routes.dashboard import dashboard_bp
    from app.routes.interview import interview_bp
    from app.routes.ai_coach import ai_coach_bp
    from app.routes.audio import audio_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(interview_bp)
    app.register_blueprint(ai_coach_bp)
    app.register_blueprint(audio_bp)
    app.register_blueprint(auth_bp)

    # Create tables and seed initial data within app context
    with app.app_context():
        db.create_all()
        DatabaseService.seed_initial_data_if_empty()

    return app

