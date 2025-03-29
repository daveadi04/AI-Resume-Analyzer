from flask import Blueprint, request, jsonify
from services.linkedin_service import LinkedInService
from config import Config

bp = Blueprint('linkedin', __name__, url_prefix='/api/linkedin')
linkedin_service = LinkedInService()

@bp.route('/analyze', methods=['POST'])
def analyze_profile():
    data = request.get_json()
    if not data or 'profile_url' not in data:
        return jsonify({"error": "LinkedIn profile URL is required"}), 400
    
    try:
        analysis = linkedin_service.analyze_profile(data['profile_url'])
        return jsonify(analysis)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/optimize', methods=['POST'])
def optimize_profile():
    data = request.get_json()
    if not data or 'profile_data' not in data:
        return jsonify({"error": "Profile data is required"}), 400
    
    try:
        optimization = linkedin_service.optimize_profile(data['profile_data'])
        return jsonify(optimization)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/generate-post', methods=['POST'])
def generate_post():
    data = request.get_json()
    if not data or 'topic' not in data:
        return jsonify({"error": "Topic is required"}), 400
    
    try:
        post = linkedin_service.generate_post(
            topic=data['topic'],
            tone=data.get('tone', 'professional'),
            length=data.get('length', 'medium')
        )
        return jsonify(post)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/suggest-keywords', methods=['POST'])
def suggest_keywords():
    data = request.get_json()
    if not data or 'profile_data' not in data:
        return jsonify({"error": "Profile data is required"}), 400
    
    try:
        keywords = linkedin_service.suggest_keywords(data['profile_data'])
        return jsonify(keywords)
    except Exception as e:
        return jsonify({"error": str(e)}), 500 