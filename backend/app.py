from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from routes.resume_routes import resume_bp
from routes.portfolio_routes import portfolio_bp
from routes.social_routes import social_bp
from routes.interview_routes import interview_bp
from services.resume_service import ResumeService
from services.portfolio_service import PortfolioService
from services.social_service import SocialService
from services.interview_service import InterviewService

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Enable CORS for all routes with specific configuration
CORS(app, 
     resources={
         r"/api/*": {
             "origins": ["http://localhost:3000"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "supports_credentials": True
         }
     })

# Initialize services
resume_service = ResumeService()
portfolio_service = PortfolioService()
social_service = SocialService()
interview_service = InterviewService()

# Register blueprints with URL prefixes
app.register_blueprint(resume_bp, url_prefix="/api/resume")
app.register_blueprint(portfolio_bp, url_prefix="/api/portfolio")
app.register_blueprint(social_bp, url_prefix="/api/social")
app.register_blueprint(interview_bp, url_prefix="/api/interview")

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to AI Personal Branding Assistant API",
        "status": "active"
    })

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "version": "1.0.0"
    })

# Handle OPTIONS method for CORS preflight
@app.route('/api/<path:path>', methods=['OPTIONS'])
def options_handler(path):
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=5000)
