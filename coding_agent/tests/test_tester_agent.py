"""
Tests for the Tester Agent
"""
import pytest
from unittest.mock import MagicMock
from coding_agent.agents.tester_agent import TesterAgent
from coding_agent.core.llm_client import LLMClient
from coding_agent.core.prompt_manager import PromptManager

def test_generate_tests():
    """Test the generate_tests method"""
    # Create mocks
    llm_client = MagicMock(spec=LLMClient)
    prompt_manager = MagicMock(spec=PromptManager)

    # Create the agent
    agent = TesterAgent(llm_client, prompt_manager)

    # Set up the mocks
    code = "def add(a, b):\n    return a + b"
    prompt = "Generate unit tests for the following code:\n\n{code}\n\n..."
    llm_client.generate.return_value = "import pytest\ndef test_add():\n    assert add(1, 2) == 3"

    # Call the method
    result = agent.generate_unit_tests(code)

    # Check the result
    assert "test_add" in result

    # Check that the mocks were called
    llm_client.generate.assert_called_once()
    prompt_manager.get_prompt.assert_called_once_with("generate_tests")

def test_generate_mocks():
    """Test the generate_mocks method"""
    # Create mocks
    llm_client = MagicMock(spec=LLMClient)
    prompt_manager = MagicMock(spec=PromptManager)

    # Create the agent
    agent = TesterAgent(llm_client, prompt_manager)

    # Set up the mocks
    code = "def add(a, b):\n    return a + b"
    prompt = "Generate mocks for the following code:\n\n{code}\n\n..."
    llm_client.generate.return_value = "from unittest.mock import MagicMock\ndef test_add_with_mock():\n    mock = MagicMock()\n    mock.return_value = 3\n    assert add(1, 2) == 3"

    # Call the method
    result = agent.generate_mocks(code)

    # Check the result
    assert "test_add_with_mock" in result

    # Check that the mocks were called
    llm_client.generate.assert_called_once()
    prompt_manager.get_prompt.assert_called_once_with("generate_mocks")