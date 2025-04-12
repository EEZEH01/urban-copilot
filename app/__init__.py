# __init__.py

from flask import Flask
from config import config  # Import the configuration from config.py

def create_app():
    app = Flask(__name__)

    # Load the configuration from the config.py file
    app.config.from_object(config)  # This applies the configuration settings to the Flask app

    return app

