"""
Tests for the API
"""
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from coding_agent.api.routes import app

client = TestClient(app)

@patch('coding_agent.api.routes.programmer_agent')
@patch('coding_agent.api.routes.tester_agent')
def test_generate_code(mock_tester_agent, mock_programmer_agent):
    """Test the generate_code endpoint"""
    # Set up the mocks
    mock_programmer_agent.analyze_requirements.return_value = '{"spec": "test"}'
    mock_programmer_agent.generate_code.return_value = 'def add(a, b):\n    return a + b'
    mock_programmer_agent.create_documentation.return_value = 'Documentation'
    mock_tester_agent.generate_unit_tests.return_value = 'import pytest\ndef test_add():\n    assert add(1, 2) == 3'

    # Set up the request
    requirements = "Create a simple web application with user authentication and a dashboard"

    # Call the endpoint
    response = client.post("/generate_code", json={"requirements": requirements})

    # Check the response
    assert response.status_code == 200
    assert "code" in response.json()
    assert response.json()["code"] == 'def add(a, b):\n    return a + b'

@patch('coding_agent.api.routes.validator_agent')
def test_validate_code(mock_validator_agent):
    """Test the validate_code endpoint"""
    # Set up the mocks
    mock_validator_agent.static_analysis.return_value = 'Analysis'
    mock_validator_agent.security_check.return_value = 'Security'
    mock_validator_agent.validate_standards.return_value = 'Standards'

    # Set up the request
    code = "def add(a, b):\n    return a + b"

    # Call the endpoint
    response = client.post("/validate_code", json={"code": code})

    # Check the response
    assert response.status_code == 200
    assert "analysis" in response.json()