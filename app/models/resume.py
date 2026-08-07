from datetime import datetime, timezone
from app.models.user import db

class ResumeAnalysis(db.Model):
    __tablename__ = 'resume_analyses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, default=1)
    target_job_title = db.Column(db.String(120), nullable=False)
    resume_text = db.Column(db.Text, nullable=False)
    match_score = db.Column(db.Integer, nullable=False, default=78) # Percentage match
    strengths = db.Column(db.Text, nullable=True) # JSON or comma separated
    missing_skills = db.Column(db.Text, nullable=True)
    recommendations = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'target_job_title': self.target_job_title,
            'match_score': self.match_score,
            'strengths': [s.strip() for s in self.strengths.split(';') if s.strip()] if self.strengths else [],
            'missing_skills': [s.strip() for s in self.missing_skills.split(';') if s.strip()] if self.missing_skills else [],
            'recommendations': [s.strip() for s in self.recommendations.split(';') if s.strip()] if self.recommendations else [],
            'created_at': self.created_at.strftime('%b %d, %Y')
        }
