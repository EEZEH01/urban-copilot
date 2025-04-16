# app/__init__.py
import os
from flask import Flask, send_from_directory
from app.routes import urban_bp  # Import the Blueprint from the routes module
from app.swagger import swagger_ui_blueprint, SWAGGER_URL  # Import Swagger UI blueprint
from app.limiter import configure_limiter  # Import rate limiter configuration

def create_app():
    """
    Create and configure the Flask application.

    This function initializes the Flask app, registers the routes (via Blueprint),
    and sets up any necessary configurations.
    """
    # Create a new Flask app instance with static folder at the project root
    app = Flask(__name__, static_folder=None)
    
    # Register the Blueprint with the app
    # The 'urban_bp' blueprint contains all the routes related to urban topics
    app.register_blueprint(urban_bp)  # Registering at root level for proper URL routing
    
    # Register Swagger UI Blueprint
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
    
    # Configure rate limiting
    configure_limiter(app)
    
    # Serve static files from the static directory
    @app.route('/static/<path:path>')
    def serve_static(path):
        return send_from_directory('../static', path)
    
    # Serve the main index.html file
    @app.route('/')
    def index():
        return send_from_directory('../static', 'index.html')
    
    # Optional: Additional configurations or middlewares can be set here
    # Load configurations from environment variables
    app.config.from_pyfile('config.py')

    return app



