import os
import uuid
from pathlib import Path
from flask import current_app

class TTSService:
    """
    Text-To-Speech Service.
    Generates audio files using gTTS (Google Text-To-Speech) or formats payload for Web Speech Synthesis.
    """

    @staticmethod
    def text_to_speech_file(text, lang='en'):
        """Converts text into an MP3 file saved in app static folder."""
        if not text or len(text.strip()) == 0:
            return None

        try:
            from gtts import gTTS
            
            # Ensure upload directory exists
            upload_dir = Path(current_app.config['UPLOAD_FOLDER']) / 'audio'
            upload_dir.mkdir(parents=True, exist_ok=True)
            
            filename = f"tts_{uuid.uuid4().hex[:10]}.mp3"
            filepath = upload_dir / filename
            
            # Truncate text if too long for quick speech generation
            speak_text = text[:400]
            tts = gTTS(text=speak_text, lang=lang, slow=False)
            tts.save(str(filepath))
            
            return f"/static/uploads/audio/{filename}"
        except Exception as e:
            print(f"[TTSService] Warning: gTTS file generation skipped: {e}")
            return None

    @staticmethod
    def get_speech_payload(text):
        """Prepares text payload for client browser speech synth synthesis."""
        return {
            "text": text,
            "lang": "en-US",
            "rate": 1.0,
            "pitch": 1.0
        }
