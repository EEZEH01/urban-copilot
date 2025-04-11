import sys
import os
import logging

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Flask server for Urban Copilot
from flask import Flask, request, jsonify
from app.agents import UrbanAgent

app = Flask(__name__)
agent = UrbanAgent()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.before_request
def log_request_info():
    logger.info(f"Request: {request.method} {request.url}")

@app.after_request
def log_response_info(response):
    logger.info(f"Response: {response.status_code} {response.get_data(as_text=True)}")
    return response

@app.route('/')
def home():
    return "Welcome to Urban Copilot!"

@app.route('/favicon.ico')
def favicon():
    return "", 204

# Add route to interact with UrbanAgent
@app.route('/api/respond', methods=['POST'])
def respond():
    user_input = request.json.get('message', '')
    if not user_input:
        return jsonify({'error': 'Message is required'}), 400

    response = agent.respond(user_input)
    return jsonify({'response': response})

# Serve static files
@app.route('/static/<path:filename>')
def static_files(filename):
    return app.send_static_file(filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
