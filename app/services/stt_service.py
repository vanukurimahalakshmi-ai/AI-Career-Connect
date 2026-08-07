import os
import re

class STTService:
    """
    Speech-To-Text Service.
    Handles transcript normalization, audio transcript processing, and keyword extraction.
    """
    
    @staticmethod
    def process_transcript(raw_text):
        """Clean and normalize transcribed speech text."""
        if not raw_text:
            return ""

        # Remove extra whitespace and format sentences
        cleaned = re.sub(r'\s+', ' ', raw_text.strip())
        if cleaned and not cleaned[0].isupper():
            cleaned = cleaned[0].upper() + cleaned[1:]
        if cleaned and cleaned[-1] not in ['.', '?', '!']:
            cleaned += '.'
            
        return cleaned

    @staticmethod
    def extract_key_phrases(transcript):
        """Extract important technical keywords from user speech."""
        keywords = ["architecture", "flask", "sqlite", "python", "api", "ai", "mistral", "database", "performance", "scaling", "speech", "design", "system"]
        found = []
        lower_trans = transcript.lower()
        for kw in keywords:
            if kw in lower_trans:
                found.append(kw.capitalize())
        return list(set(found))
