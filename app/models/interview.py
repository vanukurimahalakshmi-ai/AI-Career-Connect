from datetime import datetime, timezone
from app.models.user import db

class InterviewSession(db.Model):
    __tablename__ = 'interview_sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, default=1)
    target_role = db.Column(db.String(100), nullable=False, default="Software Engineer")
    topic = db.Column(db.String(100), nullable=False, default="Technical Behavioral & Architecture")
    status = db.Column(db.String(30), default="Completed") # 'In Progress', 'Completed'
    score = db.Column(db.Integer, default=85) # 0-100 score
    summary_feedback = db.Column(db.Text, default="Solid architectural explanations. Could improve depth on concurrency trade-offs.")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship to conversation transcripts
    transcripts = db.relationship('InterviewTranscript', backref='session', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'target_role': self.target_role,
            'topic': self.topic,
            'status': self.status,
            'score': self.score,
            'summary_feedback': self.summary_feedback,
            'created_at': self.created_at.strftime('%b %d, %Y %H:%M'),
            'transcripts_count': len(self.transcripts)
        }


class InterviewTranscript(db.Model):
    __tablename__ = 'interview_transcripts'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('interview_sessions.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    user_response_text = db.Column(db.Text, nullable=True) # captured from Speech to Text (STT)
    audio_path = db.Column(db.String(255), nullable=True) # stored audio recording filepath if saved
    ai_feedback = db.Column(db.Text, nullable=True) # AI analysis of candidate response
    ai_audio_url = db.Column(db.String(255), nullable=True) # generated audio url (Text to Speech)
    score = db.Column(db.Integer, default=80)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'question': self.question,
            'user_response_text': self.user_response_text,
            'audio_path': self.audio_path,
            'ai_feedback': self.ai_feedback,
            'ai_audio_url': self.ai_audio_url,
            'score': self.score,
            'created_at': self.created_at.strftime('%H:%M:%S')
        }
