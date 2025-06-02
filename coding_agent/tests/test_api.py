"""
Tests for the API
"""
import pytest
from fastapi.testclient import TestClient
from api.routes import app

client = TestClient(app)

def test_generate_code():
    """Test the generate_code endpoint"""
    # Set up the request
    requirements = "Create a simple web application with user authentication and a dashboard"

    # Call the endpoint
    response = client.post("/generate_code", json={"requirements": requirements})

    # Check the response
    assert response.status_code == 200
    assert "code" in response.json()

def test_validate_code():
    """Test the validate_code endpoint"""
    # Set up the request
    code = "def add(a, b):\n    return a + b"

    # Call the endpoint
    response = client.post("/validate_code", json={"code": code})

    # Check the response
    assert response.status_code == 200
    assert "analysis" in response.json()