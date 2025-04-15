# app/__init__.py
from flask import Flask
from app.routes import urban_bp  # Import the Blueprint from the routes module

def create_app():
    """
    Create and configure the Flask application.

    This function initializes the Flask app, registers the routes (via Blueprint),
    and sets up any necessary configurations.
    """
    app = Flask(__name__)  # Create a new Flask app instance
    
    # Register the Blueprint with the app
    # The 'urban_bp' blueprint contains all the routes related to urban topics
    app.register_blueprint(urban_bp, url_prefix='/urban')  # Optional: add a URL prefix

    # Optional: Additional configurations or middlewares can be set here
    # For example, app.config.from_pyfile('config.py')

    return app



