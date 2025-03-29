from flask import Blueprint, request, jsonify
from services.social_service import SocialService
from config import Config

# Define the blueprint with the correct name
social_bp = Blueprint('social', __name__, url_prefix='/api/social')
social_service = SocialService()

@social_bp.route('/generate-post', methods=['POST'])
def generate_post():
    """
    Endpoint for generating social media posts
    """
    data = request.get_json()
    if not data or 'topic' not in data:
        return jsonify({'error': 'Topic is required'}), 400
    
    try:
        result = social_service.generate_post(
            topic=data['topic'],
            platform=data.get('platform', 'linkedin'),
            tone=data.get('tone', 'professional'),
            length=data.get('length', 'medium')
        )
        return jsonify(result)
    except Exception as e:
        print(f"Error generating post: {str(e)}")
        return jsonify({'error': str(e)}), 500

@social_bp.route('/generate-thread', methods=['POST'])
def generate_thread():
    """
    Endpoint for generating social media threads
    """
    data = request.get_json()
    if not data or 'topic' not in data:
        return jsonify({'error': 'Topic is required'}), 400
    
    try:
        result = social_service.generate_thread(
            topic=data['topic'],
            platform=data.get('platform', 'twitter')
        )
        return jsonify(result)
    except Exception as e:
        print(f"Error generating thread: {str(e)}")
        return jsonify({'error': str(e)}), 500

@social_bp.route('/suggest-hashtags', methods=['POST'])
def suggest_hashtags():
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({"error": "Content is required"}), 400
    
    try:
        hashtags = social_service.suggest_hashtags(
            content=data['content'],
            platform=data.get('platform', 'linkedin')
        )
        return jsonify(hashtags)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@social_bp.route('/optimize-timing', methods=['POST'])
def optimize_timing():
    data = request.get_json()
    if not data or 'platform' not in data:
        return jsonify({"error": "Platform is required"}), 400
    
    try:
        timing = social_service.optimize_posting_time(
            platform=data['platform'],
            timezone=data.get('timezone', 'UTC')
        )
        return jsonify(timing)
    except Exception as e:
        return jsonify({"error": str(e)}), 500 