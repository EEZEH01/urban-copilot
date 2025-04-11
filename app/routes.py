from flask import request, jsonify
from app.agents import UrbanAgent

agent = UrbanAgent()

def register_routes(app):

    @app.before_request
    def log_request():
        app.logger.info(f"Request: {request.method} {request.url}")

    @app.after_request
    def log_response(response):
        app.logger.info(f"Response: {response.status_code}")
        return response

    @app.route("/api/ask", methods=["POST"])
    def ask():
        data = request.json
        question = data.get("question")
        response = agent.ask(question)
        return jsonify({"response": response})
