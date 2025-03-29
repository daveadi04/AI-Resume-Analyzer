from flask import Blueprint, request, jsonify
from services.portfolio_service import PortfolioService
from config import Config

portfolio_bp = Blueprint('portfolio', __name__, url_prefix='/api/portfolio')
portfolio_service = PortfolioService()

@portfolio_bp.route('/generate', methods=['POST'])
def generate_portfolio():
    data = request.get_json()
    if not data or 'user_data' not in data:
        return jsonify({"error": "User data is required"}), 400
    
    try:
        portfolio = portfolio_service.generate_portfolio(data['user_data'])
        return jsonify(portfolio)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@portfolio_bp.route('/analyze-github', methods=['POST'])
def analyze_github():
    data = request.get_json()
    if not data or 'github_username' not in data:
        return jsonify({"error": "GitHub username is required"}), 400
    
    try:
        analysis = portfolio_service.analyze_github_profile(data['github_username'])
        return jsonify(analysis)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@portfolio_bp.route('/customize', methods=['POST'])
def customize_portfolio():
    data = request.get_json()
    if not data or 'portfolio_data' not in data or 'customization' not in data:
        return jsonify({"error": "Portfolio data and customization options are required"}), 400
    
    try:
        customized = portfolio_service.customize_portfolio(
            portfolio_data=data['portfolio_data'],
            customization=data['customization']
        )
        return jsonify(customized)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@portfolio_bp.route('/deploy', methods=['POST'])
def deploy_portfolio():
    data = request.get_json()
    if not data or 'portfolio_data' not in data:
        return jsonify({"error": "Portfolio data is required"}), 400
    
    try:
        deployment = portfolio_service.deploy_portfolio(data['portfolio_data'])
        return jsonify(deployment)
    except Exception as e:
        return jsonify({"error": str(e)}), 500 