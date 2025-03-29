import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    LINKEDIN_API_KEY = os.getenv('LINKEDIN_API_KEY')
    GITHUB_API_KEY = os.getenv('GITHUB_API_KEY')
    TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/ai_branding')
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key')
    
    # OpenAI Settings
    OPENAI_MODEL = "gpt-4"
    OPENAI_TEMPERATURE = 0.7
    
    # File Upload Settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
    
    # API Rate Limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URL = "memory://"
    RATELIMIT_STRATEGY = "fixed-window"
    RATELIMIT_DEFAULT = "100 per minute" 