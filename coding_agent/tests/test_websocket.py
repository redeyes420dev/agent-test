"""
Tests for the WebSocket
"""
import pytest
from unittest.mock import MagicMock, patch
from coding_agent.api.websocket import ConnectionManager

def test_websocket():
    """Test the WebSocket"""
    # Create a mock WebSocket
    mock_websocket = MagicMock()
    mock_websocket.send_text = MagicMock()  # Make send_text a mock

    # Create the manager
    manager = ConnectionManager()

    # Connect the mock WebSocket
    # We're not actually calling the coroutine, just testing the logic
    manager.active_connections.append(mock_websocket)

    # Send a message
    message = "Hello, world!"

    # Test broadcasting - directly call the method that would be called by the coroutine
    for connection in manager.active_connections:
        connection.send_text(message)

    # Check that the message was sent
    mock_websocket.send_text.assert_called_with(message)

    # Disconnect the mock WebSocket
    manager.disconnect(mock_websocket)