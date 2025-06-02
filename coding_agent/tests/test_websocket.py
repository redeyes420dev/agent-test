"""
Tests for the WebSocket
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from api.routes import app
from api.websocket import manager

client = TestClient(app)

def test_websocket():
    """Test the WebSocket"""
    # Set up the WebSocket
    with client.websocket_connect("/ws") as websocket:
        # Send a message
        websocket.send_json({"message": "Hello, world!"})

        # Receive a response
        response = websocket.receive_json()

        # Check the response
        assert response["message"] == "Hello, world!"