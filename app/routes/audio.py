from flask import Blueprint, jsonify, request, send_from_directory, current_app
import os
from app.services.tts_service import TTSService
from app.services.stt_service import STTService

audio_bp = Blueprint('audio', __name__)

@audio_bp.route('/api/tts/speak', methods=['POST'])
def tts_speak():
    """Generates audio on the fly for given text string."""
    data = request.json or {}
    text = data.get('text', '')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    audio_url = TTSService.text_to_speech_file(text)
    payload = TTSService.get_speech_payload(text)

    return jsonify({
        "status": "success",
        "audio_url": audio_url,
        "tts_payload": payload
    })

@audio_bp.route('/api/stt/transcribe', methods=['POST'])
def stt_transcribe():
    """Endpoint for normalizing and extracting keywords from browser STT input."""
    data = request.json or {}
    raw_transcript = data.get('transcript', '')

    cleaned = STTService.process_transcript(raw_transcript)
    keywords = STTService.extract_key_phrases(cleaned)

    return jsonify({
        "status": "success",
        "cleaned_transcript": cleaned,
        "keywords": keywords
    })
