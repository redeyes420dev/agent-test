"""
Tests for the LLM Client
"""
import pytest
from coding_agent.core.llm_client import LLMClient

def test_generate():
    """Test the generate method"""
    # Create the client
    client = LLMClient(api_key="your-openai-api-key")

    # Set up the prompt
    prompt = "Generate a simple Python function"

    # Call the method
    result = client.generate(prompt)

    # Check the result
    assert result is not None
    assert isinstance(result, str)