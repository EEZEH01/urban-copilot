import logging
from flask import Flask, request, jsonify
from app.agents import UrbanAgent

app = Flask(__name__)
agent = UrbanAgent()

# Logging config
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.before_request
def log_request_info():
    logger.info(f"Request: {request.method} {request.url}")

@app.after_request
def log_response_info(response):
    logger.info(f"Response: {response.status_code}")
    return response

# Endpoint ejemplo
@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_question = data.get("question")
    answer = agent.ask(user_question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)

