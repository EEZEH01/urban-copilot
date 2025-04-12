from flask import Flask
from app.api.routes import api  # Blueprint import

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api, url_prefix="/api")
    return app
