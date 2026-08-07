from datetime import datetime, timezone
from app.models.user import db

class CareerGoal(db.Model):
    __tablename__ = 'career_goals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, default=1)
    goal_title = db.Column(db.String(150), nullable=False)
    target_date = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(30), default="In Progress") # 'In Progress', 'Completed'
    progress_percentage = db.Column(db.Integer, default=40)
    milestones = db.Column(db.Text, nullable=True) # Semicolon delimited JSON/string list
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'goal_title': self.goal_title,
            'target_date': self.target_date,
            'status': self.status,
            'progress_percentage': self.progress_percentage,
            'milestones': [m.strip() for m in self.milestones.split(';') if m.strip()] if self.milestones else [],
            'created_at': self.created_at.strftime('%b %d, %Y')
        }
