import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import pytest
from app.server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to Urban Copilot!" in response.data

def test_favicon_route(client):
    response = client.get('/favicon.ico')
    assert response.status_code == 204

def test_respond_route(client):
    response = client.post('/api/respond', json={'message': 'Hello'})
    assert response.status_code == 200
    assert 'response' in response.get_json()

def test_respond_route_no_message(client):
    response = client.post('/api/respond', json={})
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Message is required'
