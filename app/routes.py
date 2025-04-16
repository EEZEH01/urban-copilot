from flask import Blueprint, request, jsonify
from app.agents.urban_agent import UrbanAgent

# Create a Blueprint for urban planning routes
urban_bp = Blueprint('urban', __name__)

# Initialize the urban agent
urban_agent = UrbanAgent()

@urban_bp.route('/api/ask', methods=['POST'])
def ask_urban_question():
    """
    Endpoint to ask urban planning questions.
    Expects a JSON payload with a 'question' field.
    """
    data = request.get_json()
    
    if not data or 'question' not in data:
        return jsonify({'error': 'Question is required'}), 400
    
    question = data['question']
    context = data.get('context', '')  # Optional context information
    
    response = urban_agent.generate_enhanced_response(question, context)
    
    return jsonify(response)

@urban_bp.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring and Docker HEALTHCHECK.
    Returns status of the application and its dependencies.
    """
    # Check if essential services are available
    health_status = {
        "status": "healthy",
        "version": "1.0.0",
        "services": {
            "api": "up",
            "cognitive_services": urban_agent.cognitive_client.is_available()
        }
    }
    
    # If any critical service is down, return unhealthy status
    if not all(status == "up" for service, status in health_status["services"].items()):
        health_status["status"] = "degraded"
        return jsonify(health_status), 200
        
    return jsonify(health_status)



