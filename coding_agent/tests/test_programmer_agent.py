"""
Tests for the Programmer Agent
"""
import pytest
from unittest.mock import MagicMock
from agents.programmer_agent import ProgrammerAgent
from core.llm_client import LLMClient
from core.prompt_manager import PromptManager

def test_analyze_requirements():
    """Test the analyze_requirements method"""
    # Create mocks
    llm_client = MagicMock(spec=LLMClient)
    prompt_manager = MagicMock(spec=PromptManager)

    # Create the agent
    agent = ProgrammerAgent(llm_client, prompt_manager)

    # Set up the mocks
    requirements = "Create a simple web application with user authentication and a dashboard"
    prompt = "Analyze the following requirements and create a technical specification:\n\n{requirements}\n\n..."
    llm_client.generate.return_value = '{"title": "Web Application", "description": "A simple web application with user authentication and a dashboard"}'

    # Call the method
    result = agent.analyze_requirements(requirements)

    # Check the result
    assert "title" in result
    assert "description" in result

    # Check that the mocks were called
    llm_client.generate.assert_called_once()
    prompt_manager.get_prompt.assert_called_once_with("analyze_requirements")

def test_generate_code():
    """Test the generate_code method"""
    # Create mocks
    llm_client = MagicMock(spec=LLMClient)
    prompt_manager = MagicMock(spec=PromptManager)

    # Create the agent
    agent = ProgrammerAgent(llm_client, prompt_manager)

    # Set up the mocks
    spec = {"title": "Web Application", "description": "A simple web application"}
    prompt = "Generate code based on the following specification:\n\n{spec}\n\n..."
    llm_client.generate.return_value = "def main():\n    print('Hello, world!')"

    # Call the method
    result = agent.generate_code(spec)

    # Check the result
    assert "def main()" in result

    # Check that the mocks were called
    llm_client.generate.assert_called_once()
    prompt_manager.get_prompt.assert_called_once_with("generate_code")