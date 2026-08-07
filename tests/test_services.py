import pytest
from app.services.stt_service import STTService
from app.services.mistral_service import MistralService

def test_stt_transcript_normalization():
    """Test STT text normalization and phrase extraction."""
    raw = "hello world flask sqlite python architecture design"
    cleaned = STTService.process_transcript(raw)
    assert cleaned.startswith("Hello")
    assert cleaned.endswith(".")

    keywords = STTService.extract_key_phrases(cleaned)
    assert "Flask" in keywords
    assert "Python" in keywords

def test_mistral_service_fallback():
    """Test Mistral AI simulation fallback when API key is empty."""
    service = MistralService(api_key="")
    q = service.generate_interview_question("AI Developer", "Coding & Algorithms", "Mid-Level")
    assert "question" in q
    assert "hints" in q

    eval_result = service.evaluate_interview_response("Question?", "I built a Flask backend using SQLite and Mistral API.", "AI Developer")
    assert eval_result['score'] > 0
    assert 'feedback' in eval_result
