from flask import Blueprint, render_template, jsonify, request, current_app
from app.models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/settings')
def settings():
    """Renders user profile & API configuration page."""
    user = User.query.first()
    return render_template('settings.html', user=user, mistral_key=current_app.config.get('MISTRAL_API_KEY', ''))

@auth_bp.route('/api/settings/save', methods=['POST'])
def save_settings():
    """Saves API key and profile preferences."""
    data = request.json or {}
    api_key = data.get('mistral_api_key', '').strip()
    
    if api_key:
        current_app.config['MISTRAL_API_KEY'] = api_key
        os_env_file = current_app.config['BASE_DIR'] / '.env' if 'BASE_DIR' in current_app.config else None

    user = User.query.first()
    if user:
        user.target_role = data.get('target_role', user.target_role)
        user.experience_level = data.get('experience_level', user.experience_level)
        user.skills = data.get('skills', user.skills)
        user.bio = data.get('bio', user.bio)
        db.session.commit()

    return jsonify({"status": "success", "message": "Settings updated successfully!"})
