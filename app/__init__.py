# app/__init__.py
from flask import Flask
from app.routes import urban_bp  # Import the Blueprint

def create_app():
    """
    Create and configure the Flask application.

    This function initializes the Flask app and registers the routes.
    """
    app = Flask(__name__)  # Create a new Flask app instance
    
    # Register the Blueprint with the app
    app.register_blueprint(urban_bp)

    return app


