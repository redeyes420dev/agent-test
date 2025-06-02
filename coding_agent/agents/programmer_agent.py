"""
Programmer Agent - Generates code based on user requirements
"""
import json
from typing import Dict, Any
from core.llm_client import LLMClient
from core.prompt_manager import PromptManager

class ProgrammerAgent:
    def __init__(self, llm_client: LLMClient, prompt_manager: PromptManager):
        self.llm_client = llm_client
        self.prompt_manager = prompt_manager

    def analyze_requirements(self, requirements: str) -> Dict[str, Any]:
        """Analyze requirements and create a technical specification"""
        prompt = self.prompt_manager.get_prompt("analyze_requirements")
        input_data = {"requirements": requirements}
        response = self.llm_client.generate(prompt, input_data)
        return json.loads(response)

    def generate_code(self, spec: Dict[str, Any], language: str = "python") -> str:
        """Generate code based on a technical specification"""
        prompt = self.prompt_manager.get_prompt("generate_code")
        input_data = {"spec": spec, "language": language}
        response = self.llm_client.generate(prompt, input_data)
        return response

    def create_documentation(self, code: str) -> str:
        """Generate documentation for the given code"""
        prompt = self.prompt_manager.get_prompt("create_documentation")
        input_data = {"code": code}
        response = self.llm_client.generate(prompt, input_data)
        return response

    def refactor_code(self, code: str) -> str:
        """Refactor the given code to improve its structure and performance"""
        prompt = self.prompt_manager.get_prompt("refactor_code")
        input_data = {"code": code}
        response = self.llm_client.generate(prompt, input_data)
        return response

    def optimize_code(self, code: str) -> str:
        """Optimize the given code for better performance"""
        prompt = self.prompt_manager.get_prompt("optimize_code")
        input_data = {"code": code}
        response = self.llm_client.generate(prompt, input_data)
        return response