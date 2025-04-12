import sys
import os

# Add the root directory to the Python path so that modules can be imported correctly.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app.server import app

# Pytest fixture to create a test client for the Flask application.
@pytest.fixture
def client():
    # Set the testing configuration for the app.
    app.config['TESTING'] = True
    # Create a test client that can be used to simulate HTTP requests.
    with app.test_client() as client:
        yield client  # The test functions will receive this client.

# Test for the home route; it verifies that the home route returns status 200 and the expected content.
def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to Urban Copilot!" in response.data

# Test for the favicon route; it verifies that the favicon route returns status 204 (No Content).
def test_favicon_route(client):
    response = client.get('/favicon.ico')
    assert response.status_code == 204

# Test for the respond route; it sends a POST request with a valid message and checks if the response includes a 'response' key.
def test_respond_route(client):
    response = client.post('/api/respond', json={'message': 'Hello'})
    assert response.status_code == 200
    assert 'response' in response.get_json()

# Test for the respond route when no message is provided; it expects an error with status 400 and a specific error message.
def test_respond_route_no_message(client):
    response = client.post('/api/respond', json={})
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Message is required'

