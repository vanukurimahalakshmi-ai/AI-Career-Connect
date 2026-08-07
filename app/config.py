import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ai-career-connect-secret-key-default')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{BASE_DIR / "instance" / "app.db"}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Mistral API Configuration
    MISTRAL_API_KEY = os.environ.get('MISTRAL_API_KEY', '')
    MISTRAL_MODEL = os.environ.get('MISTRAL_MODEL', 'mistral-small-latest')
    
    # Audio Upload Path
    UPLOAD_FOLDER = BASE_DIR / 'app' / 'static' / 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max limit
