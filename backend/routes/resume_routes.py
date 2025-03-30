from flask import Blueprint, request, jsonify # type: ignore
from werkzeug.utils import secure_filename # type: ignore
import os
from services.resume_service import ResumeService
from config import Config

# Create uploads directory if it doesn't exist
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

# Change the blueprint name to match the import
resume_bp = Blueprint('resume', __name__)
resume_service = ResumeService()

@resume_bp.route('/analyze', methods=['POST'])
def analyze_resume():
    """
    Endpoint for resume analysis
    """
    if 'resume' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['resume']
    job_description = request.form.get('job_description', '')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Check file type
        allowed_extensions = {'pdf', 'doc', 'docx'}
        if not '.' in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({'error': 'Invalid file type. Please upload a PDF, DOC, or DOCX file.'}), 400

        # Create a secure filename and ensure the path exists
        filename = secure_filename(file.filename)
        filepath = os.path.join(os.path.abspath(Config.UPLOAD_FOLDER), filename)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save the file
        file.save(filepath)
        
        try:
            result = resume_service.analyze_resume(filepath, job_description)
            
            # Clean up the uploaded file after analysis
            try:
                os.remove(filepath)
            except:
                pass  # Ignore cleanup errors
                
            return jsonify(result)
        except Exception as e:
            # Clean up the uploaded file in case of analysis error
            try:
                os.remove(filepath)
            except:
                pass
            raise e
            
    except Exception as e:
        print(f"Error analyzing resume: {str(e)}")
        return jsonify({'error': str(e)}), 500

@resume_bp.route('/generate', methods=['POST'])
def generate_resume():
    """
    Endpoint for resume generation
    """
    data = request.get_json()
    if not data or 'job_description' not in data:
        return jsonify({'error': 'No job description provided'}), 400
    
    try:
        result = resume_service.generate_resume(data['job_description'])
        return jsonify(result)
    except Exception as e:
        print(f"Error generating resume: {str(e)}")
        return jsonify({'error': str(e)}), 500

@resume_bp.route('/cover-letter', methods=['POST'])
def generate_cover_letter():
    data = request.get_json()
    if not data or 'job_description' not in data or 'resume' not in data:
        return jsonify({"error": "Job description and resume are required"}), 400
    
    try:
        cover_letter = resume_service.generate_cover_letter(
            job_description=data['job_description'],
            resume=data['resume']
        )
        return jsonify(cover_letter)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS 