"""
Rate limiting configuration for Urban Copilot API.
This prevents abuse and ensures fair usage of the API.
"""

from flask import request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize the rate limiter
limiter = Limiter(
    key_func=get_remote_address,  # Rate limit by IP address
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",  # In-memory storage for development
)

def configure_limiter(app):
    """
    Configure the rate limiter with the Flask application.
    
    Args:
        app: The Flask application instance
    """
    limiter.init_app(app)
    
    # Apply specific rate limits to endpoints that are resource-intensive
    limiter.limit("10 per minute")(app.view_functions['urban.ask_urban_question'])
    
    # The health check and docs endpoints don't need strict rate limiting
    limiter.exempt(app.view_functions['urban.health_check'])
