import sys
import os

# Add the root directory to the Python path so that modules can be imported correctly.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sys
import os
import pytest
from app.server import app

# Add the root directory to the Python path so that modules can be imported correctly.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Pytest fixture to create a test client for the Flask application.
@pytest.fixture
def client():
    """
    Fixture to create a test client for simulating HTTP requests.
    It sets the app configuration to 'TESTING' mode, allowing for better error reporting.
    """
    app.config['TESTING'] = True
    # Create a test client for making requests to the app
    with app.test_client() as client:
        yield client  # The test functions will receive this client.

# Test for the home route; it verifies that the home route returns status 200 and the expected content.
def test_home_route(client):
    """
    Test the home route ('/') to ensure it returns status 200 and contains the expected text.
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to Urban Copilot!" in response.data  # Adjust if home content changes

# Test for the favicon route; it verifies that the favicon route returns status 204 (No Content).
def test_favicon_route(client):
    """
    Test the favicon route ('/favicon.ico') to ensure it returns status 204 (No Content).
    """
    response = client.get('/favicon.ico')
    assert response.status_code == 204  # This may change if you decide to serve a favicon

# Test for the respond route; it sends a POST request with a valid message and checks if the response includes a 'response' key.
def test_respond_route(client):
    """
    Test the '/api/respond' route with a valid message.
    Verifies that the response contains the 'response' key.
    """
    response = client.post('/api/respond', json={'message': 'Hello'})
    assert response.status_code == 200
    assert 'response' in response.get_json()  # Ensure the response contains the 'response' key

# Test for the respond route when no message is provided; it expects an error with status 400 and a specific error message.
def test_respond_route_no_message(client):
    """
    Test the '/api/respond' route when no message is provided in the request body.
    Expects a 400 error with the message 'Message is required'.
    """
    response = client.post('/api/respond', json={})
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Message is required'  # Error message when 'message' is missing

# Additional test for handling invalid data (non-string input).
def test_respond_route_invalid_data(client):
    """
    Test the '/api/respond' route with invalid data (non-string input).
    Should return a 400 error indicating invalid message type.
    """
    response = client.post('/api/respond', json={'message': 12345})  # Sending an integer instead of a string
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Invalid message type, expected a string'

# Test for handling an empty POST request.
def test_respond_route_empty_post(client):
    """
    Test the '/api/respond' route with an empty POST request.
    Should return a 400 error with a clear message about the request body.
    """
    response = client.post('/api/respond', json={})  # Empty body
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Request body is empty'

# Test for handling a missing 'question' in the payload for the '/api/ask' route.
def test_ask_route_no_question(client):
    """
    Test the '/api/ask' route when no 'question' is provided in the request body.
    Expects a 400 error with the message 'No question provided'.
    """
    response = client.post('/api/ask', json={})  # Missing 'question' key
    assert response.status_code == 400
    assert response.get_json()['error'] == 'No question provided'

# Test for a valid question sent to the '/api/ask' route.
def test_ask_route_valid_question(client):
    """
    Test the '/api/ask' route with a valid 'question'.
    Verifies that the response contains the 'response' key.
    """
    response = client.post('/api/ask', json={'question': 'What is urban planning?'})
    assert response.status_code == 200
    assert 'response' in response.get_json()


