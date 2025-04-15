@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data.get("question", "").strip()

        if not question:
            return jsonify({"error": "Question cannot be empty"}), 400  # Bad request if no question is provided

        # Use the agent to get the response
        response = agent.run(question)
        return jsonify({"response": response})

    except Exception as e:
        # If something goes wrong, log the error and return a 500 Internal Server Error
        logging.error(f"Error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500  # Internal server error


