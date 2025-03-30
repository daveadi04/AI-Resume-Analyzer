from flask import Blueprint, request, jsonify
from services.interview_service import InterviewService

# Define the blueprint with the correct name
interview_bp = Blueprint('interview', __name__)
interview_service = InterviewService()

@interview_bp.route('/generate-questions', methods=['POST'])
def generate_questions():
    """
    Endpoint for generating interview questions
    """
    try:
        data = request.get_json()
        job_description = data.get('job_description')
        difficulty = data.get('difficulty', 'medium')
        
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400
            
        result = interview_service.generate_questions(job_description, difficulty)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@interview_bp.route('/generate-answers', methods=['POST'])
def generate_answers():
    """
    Endpoint for generating sample answers
    """
    try:
        data = request.get_json()
        question = data.get('question')
        job_context = data.get('job_context')
        difficulty = data.get('difficulty', 'medium')
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
            
        result = interview_service.generate_answers(question, job_context, difficulty)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@interview_bp.route('/mock-interview', methods=['POST'])
def mock_interview():
    """
    Endpoint for conducting a mock interview
    """
    data = request.get_json()
    if not data or 'job_description' not in data:
        return jsonify({'error': 'Job description is required'}), 400
    
    try:
        result = interview_service.conduct_mock_interview(
            job_description=data['job_description'],
            duration=data.get('duration', 30)
        )
        return jsonify(result)
    except Exception as e:
        print(f"Error conducting mock interview: {str(e)}")
        return jsonify({'error': str(e)}), 500

@interview_bp.route('/analyze-response', methods=['POST'])
def analyze_response():
    """
    Endpoint for analyzing a response
    """
    try:
        data = request.get_json()
        response = data.get('response')
        question = data.get('question')
        job_context = data.get('job_context')
        
        if not response or not question:
            return jsonify({'error': 'Response and question are required'}), 400
            
        result = interview_service.analyze_response(response, question, job_context)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@interview_bp.route('/generate-feedback', methods=['POST'])
def generate_feedback():
    data = request.get_json()
    if not data or 'interview_data' not in data:
        return jsonify({"error": "Interview data is required"}), 400
    
    try:
        feedback = interview_service.generate_feedback(
            interview_data=data['interview_data'],
            job_context=data.get('job_context', {})
        )
        return jsonify(feedback)
    except Exception as e:
        return jsonify({"error": str(e)}), 500 