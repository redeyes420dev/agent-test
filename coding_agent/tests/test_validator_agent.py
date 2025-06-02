"""
Tests for the Validator Agent
"""
import pytest
from unittest.mock import MagicMock
from coding_agent.agents.validator_agent import ValidatorAgent
from coding_agent.core.llm_client import LLMClient
from coding_agent.core.prompt_manager import PromptManager

def test_static_analysis():
    """Test the static_analysis method"""
    # Create mocks
    llm_client = MagicMock(spec=LLMClient)
    prompt_manager = MagicMock(spec=PromptManager)

    # Create the agent
    agent = ValidatorAgent(llm_client, prompt_manager)

    # Set up the mocks
    code = "def add(a, b):\n    return a + b"
    prompt = "Perform static analysis on the following code:\n\n{code}\n\n..."
    llm_client.generate.return_value = '{"issues": [], "score": 100}'

    # Call the method
    result = agent.static_analysis(code)

    # Check the result
    assert "issues" in result
    assert "score" in result

    # Check that the mocks were called
    llm_client.generate.assert_called_once()
    prompt_manager.get_prompt.assert_called_once_with("static_analysis")

def test_security_check():
    """Test the security_check method"""
    # Create mocks
    llm_client = MagicMock(spec=LLMClient)
    prompt_manager = MagicMock(spec=PromptManager)

    # Create the agent
    agent = ValidatorAgent(llm_client, prompt_manager)

    # Set up the mocks
    code = "def add(a, b):\n    return a + b"
    prompt = "Perform security analysis on the following code:\n\n{code}\n\n..."
    llm_client.generate.return_value = '{"vulnerabilities": [], "score": 100}'

    # Call the method
    result = agent.security_check(code)

    # Check the result
    assert "vulnerabilities" in result
    assert "score" in result

    # Check that the mocks were called
    llm_client.generate.assert_called_once()
    prompt_manager.get_prompt.assert_called_once_with("security_check")