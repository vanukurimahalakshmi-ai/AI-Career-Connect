from flask import Blueprint, render_template, jsonify, request
from app.services.database_service import DatabaseService
from app.models import User, db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
def index():
    """Renders main dynamic dashboard HTML page."""
    data = DatabaseService.get_dashboard_stats()
    return render_template('dashboard.html', data=data)

@dashboard_bp.route('/api/dashboard/stats', methods=['GET'])
def get_stats():
    """Returns dynamic stats in JSON format for realtime AJAX updates."""
    data = DatabaseService.get_dashboard_stats()
    return jsonify(data)

@dashboard_bp.route('/api/user/profile', methods=['POST'])
def update_profile():
    """Updates target career role and user profile."""
    data = request.json or {}
    user = User.query.first()
    if user:
        user.target_role = data.get('target_role', user.target_role)
        user.experience_level = data.get('experience_level', user.experience_level)
        user.skills = data.get('skills', user.skills)
        user.bio = data.get('bio', user.bio)
        db.session.commit()
        return jsonify({"status": "success", "user": user.to_dict()})
    return jsonify({"error": "User not found"}), 44
