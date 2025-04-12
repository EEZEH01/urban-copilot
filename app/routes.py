# routes.py
from flask import Blueprint, request, jsonify, current_app
from app.agents.urban_agent import UrbanAgent

api = Blueprint("api", __name__)
agent = UrbanAgent()

@api.before_app_request
def log_request():
    current_app.logger.info(f"Request: {request.method} {request.url}")

@api.after_app_request
def log_response(response):
    current_app.logger.info(f"Response: {response.status_code}")
    return response

@api.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data.get("question", "")
        if not question:
            return jsonify({"error": "No question provided"}), 400
        response = agent.run(question)  # Asegúrate que este método exista
        return jsonify({"response": response})
    except Exception as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500

