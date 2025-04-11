# app/server.py
from flask import Flask, request, jsonify
import logging
from app.agents import UrbanAgent

agent = UrbanAgent()

def create_app():
    app = Flask(__name__)
    configure_logging(app)

    @app.route('/ask', methods=['POST'])
    def ask():
        data = request.get_json()
        response = agent.run(data["question"])
        return jsonify({"response": response})

    return app


def configure_logging(app):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    @app.before_request
    def log_request_info():
        logger.info(f"Request: {request.method} {request.url}")

    @app.after_request
    def log_response_info(response):
        logger.info(f"Response: {response.status_code}")
        return response


