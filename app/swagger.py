"""Swagger configuration for the Urban Copilot API."""

from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Urban Copilot API"
    }
)
