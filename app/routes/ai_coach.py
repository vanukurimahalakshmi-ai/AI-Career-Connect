from flask import Blueprint, render_template, jsonify, request
from app.models import db, User, ResumeAnalysis, CareerGoal
from app.services.mistral_service import MistralService

ai_coach_bp = Blueprint('ai_coach', __name__)

@ai_coach_bp.route('/resume-analyzer')
def resume_page():
    """Renders resume analysis and skill gap auditing page."""
    user = User.query.first()
    past_analyses = ResumeAnalysis.query.order_by(ResumeAnalysis.created_at.desc()).all()
    return render_template('resume_analyzer.html', user=user, past_analyses=past_analyses)

@ai_coach_bp.route('/api/resume/analyze', methods=['POST'])
def analyze_resume():
    """Analyzes resume text using Mistral AI and stores breakdown in SQLite DB."""
    data = request.json or {}
    resume_text = data.get('resume_text', '')
    target_role = data.get('target_role', 'Senior AI Engineer')

    if not resume_text or len(resume_text.strip()) < 20:
        return jsonify({"error": "Please provide a valid resume text sample (min 20 characters)."}), 400

    user = User.query.first()
    mistral = MistralService()
    analysis = mistral.analyze_resume(resume_text, target_role)

    # Save to SQLite database
    record = ResumeAnalysis(
        user_id=user.id if user else 1,
        target_job_title=target_role,
        resume_text=resume_text[:2000],
        match_score=analysis.get('match_score', 80),
        strengths="; ".join(analysis.get('strengths', [])),
        missing_skills="; ".join(analysis.get('missing_skills', [])),
        recommendations="; ".join(analysis.get('recommendations', []))
    )
    db.session.add(record)
    db.session.commit()

    return jsonify({
        "status": "success",
        "result": record.to_dict()
    })

@ai_coach_bp.route('/career-roadmap')
def roadmap_page():
    """Renders career roadmap & skills generator page."""
    user = User.query.first()
    goals = CareerGoal.query.order_by(CareerGoal.created_at.desc()).all()
    return render_template('career_roadmap.html', user=user, goals=goals)

@ai_coach_bp.route('/api/roadmap/generate', methods=['POST'])
def generate_roadmap():
    """Generates structured career path using Mistral AI."""
    data = request.json or {}
    target_role = data.get('target_role', 'AI Software Engineer')
    current_level = data.get('current_level', 'Mid-Level')

    mistral = MistralService()
    roadmap = mistral.generate_career_roadmap(target_role, current_level)

    return jsonify({
        "status": "success",
        "roadmap": roadmap
    })
