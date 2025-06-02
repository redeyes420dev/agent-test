"""
Tests for the Prompt Manager
"""
import pytest
from coding_agent.core.prompt_manager import PromptManager

def test_get_prompt():
    """Test the get_prompt method"""
    # Create the manager
    manager = PromptManager()

    # Call the method
    prompt = manager.get_prompt("analyze_requirements")

    # Check the result
    assert prompt is not None
    assert isinstance(prompt, str)
    assert "requirements" in prompt