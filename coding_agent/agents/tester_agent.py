"""
Tester Agent - Creates tests for the generated code
"""
import json
from typing import Dict, Any, List
from ..core.llm_client import LLMClient
from ..core.prompt_manager import PromptManager
from ..tools.python_bash_patch_tool import get_python_bash_patch_tool

class TesterAgent:
    def __init__(self, llm_client: LLMClient, prompt_manager: PromptManager):
        self.llm_client = llm_client
        self.prompt_manager = prompt_manager
        self.tools = [get_python_bash_patch_tool()]

    def generate_tests(self, code: str) -> str:
        """Generate tests for the given code (alias for generate_unit_tests)"""
        return self.generate_unit_tests(code)

    def generate_unit_tests(self, code: str, test_framework: str = "pytest") -> str:
        """Generate unit tests for the given code"""
        prompt = self.prompt_manager.get_prompt("generate_tests")
        input_data = {"code": code, "test_framework": test_framework}
        response = self.llm_client.generate(prompt, input_data)
        return response

    def generate_integration_tests(self, code: str) -> str:
        """Generate integration tests for the given code"""
        prompt = self.prompt_manager.get_prompt("generate_integration_tests")
        input_data = {"code": code}
        response = self.llm_client.generate(prompt, input_data)
        return response

    def generate_mocks(self, code: str) -> str:
        """Generate mocks and fixtures for the given code"""
        prompt = self.prompt_manager.get_prompt("generate_mocks")
        input_data = {"code": code}
        response = self.llm_client.generate(prompt, input_data)
        return response

    def analyze_test_coverage(self, code: str) -> Dict[str, Any]:
        """Analyze test coverage for the given code"""
        prompt = self.prompt_manager.get_prompt("analyze_test_coverage")
        input_data = {"code": code}
        response = self.llm_client.generate(prompt, input_data)
        return json.loads(response)

    def generate_test_data(self, code: str) -> str:
        """Generate test data for the given code"""
        prompt = self.prompt_manager.get_prompt("generate_test_data")
        input_data = {"code": code}
        response = self.llm_client.generate(prompt, input_data)
        return response

    def solve_testing_issue(self, issue_description: str) -> Dict[str, Any]:
        """
        Solve a testing issue using the agentic workflow with tools
        """
        # Get the agentic workflow prompt
        instructions = self.prompt_manager.get_prompt("agentic_workflow")

        # Use the LLM with tools to solve the issue
        response = self.llm_client.generate_with_tools(
            instructions=instructions,
            tools=self.tools,
            input=f"Please answer the following question:\n{issue_description}"
        )

        return response