from app import create_app  # Import the Flask app creation function
import os
from dotenv import load_dotenv  # Import dotenv to load environment variables from a .env file

# Load environment variables from .env file, so we can use them in the app
load_dotenv()

# Create the Flask application by calling the create_app function
app = create_app()

if __name__ == "__main__":
    # Retrieve the debug mode and port settings from the environment, defaulting to "false" for debug and 5000 for port
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    port = int(os.environ.get("PORT", 5000))  # Get the port from environment or default to 5000

    # Output to the console that the app is running and indicate the mode and port
    print(f"✅ Urban Copilot is running at http://localhost:{port} | Debug mode: {debug_mode}")
    
    # Run the Flask application
    app.run(host="0.0.0.0", port=port, debug=debug_mode)


