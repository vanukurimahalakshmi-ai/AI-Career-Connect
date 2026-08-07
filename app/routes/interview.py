from flask import Blueprint, render_template, jsonify, request
from app.models import db, User, InterviewSession, InterviewTranscript
from app.services.mistral_service import MistralService
from app.services.stt_service import STTService
from app.services.tts_service import TTSService

interview_bp = Blueprint('interview', __name__)

@interview_bp.route('/interview')
def interview_room():
    """Renders the AI Voice Mock Interview room view."""
    user = User.query.first()
    past_sessions = InterviewSession.query.order_by(InterviewSession.created_at.desc()).all()
    return render_template('interview.html', user=user, past_sessions=past_sessions)

@interview_bp.route('/api/interview/start', methods=['POST'])
def start_session():
    """Starts a new mock interview session."""
    data = request.json or {}
    user = User.query.first()
    target_role = data.get('target_role', user.target_role if user else 'AI Engineer')
    topic = data.get('topic', 'Technical Behavioral & Architecture')

    session = InterviewSession(
        user_id=user.id if user else 1,
        target_role=target_role,
        topic=topic,
        status="In Progress",
        score=0,
        summary_feedback="Session in progress..."
    )
    db.session.add(session)
    db.session.commit()

    # Generate initial question via Mistral AI
    mistral = MistralService()
    q_data = mistral.generate_interview_question(target_role, topic, user.experience_level if user else "Mid-Level")

    # Generate audio TTS for interviewer speaking the question
    audio_url = TTSService.text_to_speech_file(q_data['question'])

    transcript = InterviewTranscript(
        session_id=session.id,
        question=q_data['question'],
        ai_audio_url=audio_url
    )
    db.session.add(transcript)
    db.session.commit()

    return jsonify({
        "status": "success",
        "session": session.to_dict(),
        "current_question": {
            "transcript_id": transcript.id,
            "question": q_data['question'],
            "hints": q_data.get('hints', []),
            "audio_url": audio_url,
            "tts_payload": TTSService.get_speech_payload(q_data['question'])
        }
    })

@interview_bp.route('/api/interview/submit_answer', methods=['POST'])
def submit_answer():
    """Receives candidate STT response, analyzes with Mistral AI, and generates TTS audio response."""
    data = request.json or {}
    transcript_id = data.get('transcript_id')
    user_speech_text = data.get('user_speech_text', '')

    transcript = db.session.get(InterviewTranscript, transcript_id)
    if not transcript:
        return jsonify({"error": "Transcript session not found"}), 404

    # Process and normalize STT speech input
    cleaned_speech = STTService.process_transcript(user_speech_text)
    transcript.user_response_text = cleaned_speech

    # Evaluate response with Mistral AI
    session = db.session.get(InterviewSession, transcript.session_id)
    mistral = MistralService()
    eval_result = mistral.evaluate_interview_response(
        question=transcript.question,
        candidate_answer=cleaned_speech,
        role=session.target_role if session else "Software Engineer"
    )

    transcript.score = eval_result.get('score', 80)
    transcript.ai_feedback = eval_result.get('feedback', 'Good answer!')

    # Convert AI feedback into TTS spoken voice audio
    ai_audio_url = TTSService.text_to_speech_file(eval_result.get('feedback'))
    transcript.ai_audio_url = ai_audio_url

    # Update session overall average score
    all_transcripts = InterviewTranscript.query.filter_by(session_id=session.id).all()
    scores = [t.score for t in all_transcripts if t.score is not None]
    if scores:
        session.score = round(sum(scores) / len(scores))
    session.status = "Completed"
    session.summary_feedback = transcript.ai_feedback

    db.session.commit()

    return jsonify({
        "status": "success",
        "evaluation": {
            "score": transcript.score,
            "feedback": transcript.ai_feedback,
            "key_takeaways": eval_result.get('key_takeaways', []),
            "audio_url": ai_audio_url,
            "tts_payload": TTSService.get_speech_payload(transcript.ai_feedback)
        },
        "session_summary": session.to_dict()
    })
