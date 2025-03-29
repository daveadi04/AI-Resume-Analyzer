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
    data = request.get_json()
    if not data or 'job_description' not in data:
        return jsonify({'error': 'Job description is required'}), 400
    
    try:
        result = interview_service.generate_questions(
            job_description=data['job_description'],
            difficulty=data.get('difficulty', 'medium'),
            count=data.get('count', 10)
        )
        return jsonify(result)
    except Exception as e:
        print(f"Error generating questions: {str(e)}")
        return jsonify({'error': str(e)}), 500

@interview_bp.route('/generate-answers', methods=['POST'])
def generate_answers():
    """
    Endpoint for generating sample answers
    """
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({'error': 'Question is required'}), 400
    
    try:
        result = interview_service.generate_answer(
            question=data['question'],
            context=data.get('context', '')
        )
        return jsonify(result)
    except Exception as e:
        print(f"Error generating answer: {str(e)}")
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
    data = request.get_json()
    if not data or 'response' not in data or 'question' not in data:
        return jsonify({"error": "Response and question are required"}), 400
    
    try:
        analysis = interview_service.analyze_response(
            response=data['response'],
            question=data['question'],
            job_context=data.get('job_context', {})
        )
        return jsonify(analysis)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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