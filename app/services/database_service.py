from app.models.user import db, User
from app.models.interview import InterviewSession, InterviewTranscript
from app.models.resume import ResumeAnalysis
from app.models.career_goal import CareerGoal

class DatabaseService:
    """
    Analytics & Database Data Aggregator for Dynamic Dashboard.
    """

    @staticmethod
    def seed_initial_data_if_empty():
        """Populates initial sample user data and metrics if database is fresh."""
        if User.query.first() is None:
            user = User(
                username="Alex Rivera",
                email="alex.rivera@example.com",
                target_role="Senior AI Engineer",
                experience_level="Mid-Senior Level",
                skills="Python, Flask, SQLite, Mistral AI, Speech Recognition, System Architecture",
                bio="Passionate engineer building voice-powered AI tools and high-scale web platforms."
            )
            db.session.add(user)
            db.session.commit()

            # Seed sample interviews
            sess1 = InterviewSession(
                user_id=user.id,
                target_role="Senior AI Engineer",
                topic="Technical Behavioral & Architecture",
                status="Completed",
                score=88,
                summary_feedback="Strong explanation of LLM pipeline latency optimization and Flask microservices design."
            )
            sess2 = InterviewSession(
                user_id=user.id,
                target_role="Senior AI Engineer",
                topic="System Design & Scalability",
                status="Completed",
                score=92,
                summary_feedback="Excellent database indexing strategy and caching model using SQLite/Redis."
            )
            db.session.add_all([sess1, sess2])
            db.session.commit()

            # Seed sample transcripts
            t1 = InterviewTranscript(
                session_id=sess1.id,
                question="How do you handle rate limits and concurrency when consuming Mistral API in Flask?",
                user_response_text="I implement asynchronous queueing with task workers and wrap API requests in exponential backoff retries.",
                ai_feedback="Outstanding architectural awareness. Mentioning retry backoffs demonstrates senior operational experience.",
                score=90
            )
            db.session.add(t1)

            # Seed sample resume
            res = ResumeAnalysis(
                user_id=user.id,
                target_job_title="Senior AI Engineer",
                resume_text="Senior Developer with 4+ years of Python, Web development, and AI integration experience.",
                match_score=85,
                strengths="Backend Systems; Python Proficiency; Web Speech API",
                missing_skills="Vector DB Indexing; Kubernetes; Distributed Tracing",
                recommendations="Add quantitative achievements in AI throughput; Highlight Mistral AI project experience"
            )
            db.session.add(res)

            # Seed sample goals
            g1 = CareerGoal(
                user_id=user.id,
                goal_title="Complete Voice AI Interview Mastery",
                target_date="End of Month",
                status="In Progress",
                progress_percentage=75,
                milestones="Pass 5 Mock Sessions; Reach 85+ Average Score; Practice STT/TTS speech clarity"
            )
            g2 = CareerGoal(
                user_id=user.id,
                goal_title="Publish Flask & Mistral Integration Portfolio",
                target_date="Next Month",
                status="In Progress",
                progress_percentage=50,
                milestones="Deploy Flask App; Integrate SQLite ORM; Configure Live Voice Studio"
            )
            db.session.add_all([g1, g2])
            db.session.commit()

    @staticmethod
    def get_dashboard_stats(user_id=1):
        """Calculates dynamic dashboard metrics and activity feed."""
        user = db.session.get(User, user_id) or User.query.first()
        if not user:
            return {}

        interviews = InterviewSession.query.filter_by(user_id=user.id).order_by(InterviewSession.created_at.desc()).all()
        resumes = ResumeAnalysis.query.filter_by(user_id=user.id).order_by(ResumeAnalysis.created_at.desc()).all()
        goals = CareerGoal.query.filter_by(user_id=user.id).all()

        total_interviews = len(interviews)
        avg_score = round(sum(i.score for i in interviews) / total_interviews) if total_interviews > 0 else 0
        latest_resume_score = resumes[0].match_score if resumes else 0
        active_goals_count = len([g for g in goals if g.status == 'In Progress'])
        
        # Skill readiness index (calculated dynamically)
        readiness_index = round((avg_score * 0.5) + (latest_resume_score * 0.5)) if (avg_score or latest_resume_score) else 75

        # Monthly progress score distribution for charts
        interview_scores = [i.score for i in interviews[:5]][::-1] or [75, 80, 85, 88, 92]
        interview_labels = [i.created_at.strftime('%b %d') for i in interviews[:5]][::-1] or ["Session 1", "Session 2", "Session 3", "Session 4", "Session 5"]

        return {
            "user": user.to_dict(),
            "stats": {
                "total_interviews": total_interviews,
                "avg_interview_score": avg_score,
                "resume_match_score": latest_resume_score,
                "active_goals": active_goals_count,
                "readiness_index": readiness_index
            },
            "chart_data": {
                "scores": interview_scores,
                "labels": interview_labels
            },
            "recent_interviews": [i.to_dict() for i in interviews[:5]],
            "latest_resume": resumes[0].to_dict() if resumes else None,
            "goals": [g.to_dict() for g in goals]
        }
