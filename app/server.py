# server.py

import logging
from flask import Flask, request, jsonify
from app.agents.urban_agent import UrbanAgent  # Specific import

# Initialize Flask App
def create_app():
    app = Flask(__name__)

    # Initialize Agent
    agent = UrbanAgent()

    # Configure Logging
    configure_logging(app)

    @app.route("/ask", methods=["POST"])
    def ask():
        data = request.get_json()
        question = data.get("question", "")
        response = agent.run(question)
        return jsonify({"response": response})

    return app


def configure_logging(app):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger(__name__)

    @app.before_request
    def log_request():
        logger.info(f"Request: {request.method} {request.url}")

    @app.after_request
    def log_response(response):
        logger.info(f"Response Status: {response.status_code}")
        return response


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)

