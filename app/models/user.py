from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, default="CareerSeeker")
    email = db.Column(db.String(120), unique=True, nullable=False, default="user@aicareerconnect.com")
    target_role = db.Column(db.String(100), default="AI Software Engineer")
    experience_level = db.Column(db.String(50), default="Mid-Level")
    skills = db.Column(db.Text, default="Python, Flask, JavaScript, Machine Learning, SQL")
    bio = db.Column(db.Text, default="Passionate software professional looking to transition into AI & Fullstack engineering roles.")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    interviews = db.relationship('InterviewSession', backref='user', lazy=True, cascade="all, delete-orphan")
    resumes = db.relationship('ResumeAnalysis', backref='user', lazy=True, cascade="all, delete-orphan")
    career_goals = db.relationship('CareerGoal', backref='user', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'target_role': self.target_role,
            'experience_level': self.experience_level,
            'skills': [s.strip() for s in self.skills.split(',') if s.strip()] if self.skills else [],
            'bio': self.bio,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
