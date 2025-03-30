from flask import Flask, request, jsonify # type: ignore
from flask_cors import CORS # type: ignore
from dotenv import load_dotenv # type: ignore
import os
from routes.resume_routes import resume_bp
from routes.portfolio_routes import portfolio_bp
from routes.social_routes import social_bp
from routes.interview_routes import interview_bp
from services.resume_service import ResumeService
from services.portfolio_service import PortfolioService
from services.social_service import SocialService
from services.interview_service import InterviewService
from werkzeug.utils import secure_filename # type: ignore

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, 
     resources={
         r"/*": {
             "origins": ["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:3003"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization", "Accept"],
             "supports_credentials": True
         }
     })

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

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

@app.route('/api/analyze-resume', methods=['POST'])
def analyze_resume():
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Get job description
        job_description = request.form.get('job_description', '')
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400

        # Check file extension
        allowed_extensions = {'pdf', 'doc', 'docx'}
        if not '.' in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({'error': 'Invalid file type. Please upload a PDF or DOC/DOCX file'}), 400

        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Ensure the upload directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        file.save(filepath)

        try:
            # Extract text based on file type
            if filename.lower().endswith('.pdf'):
                resume_text = resume_service.extract_text_from_pdf(filepath)
            elif filename.lower().endswith(('.doc', '.docx')):
                resume_text = resume_service.extract_text_from_docx(filepath)
            else:
                return jsonify({'error': 'Unsupported file format'}), 400

            if not resume_text:
                return jsonify({'error': 'Could not extract text from the file'}), 400

            # Analyze resume
            analysis_result = resume_service.analyze_resume(resume_text, job_description)
            return jsonify(analysis_result)

        finally:
            # Clean up uploaded file
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
            except Exception as e:
                print(f"Warning: Could not remove temporary file {filepath}: {str(e)}")

    except Exception as e:
        print(f"Error in analyze_resume route: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/generate-resume', methods=['POST'])
def generate_resume():
    try:
        data = request.get_json()
        job_description = data.get('job_description')
        
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400

        resume = resume_service.generate_resume(job_description)
        return jsonify(resume)

    except Exception as e:
        print(f"Error in generate_resume route: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/generate-cover-letter', methods=['POST'])
def generate_cover_letter():
    try:
        data = request.get_json()
        resume_text = data.get('resume')
        job_description = data.get('job_description')
        
        if not resume_text or not job_description:
            return jsonify({'error': 'Resume text and job description are required'}), 400

        cover_letter = resume_service.generate_cover_letter(resume_text, job_description)
        return jsonify({'cover_letter': cover_letter})

    except Exception as e:
        print(f"Error in generate_cover_letter route: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
