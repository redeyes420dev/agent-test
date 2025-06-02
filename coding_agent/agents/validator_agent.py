"""
Validator Agent - Validates code quality and fixes issues
"""
import json
from typing import Dict, Any, List
from ..core.llm_client import LLMClient
from ..core.prompt_manager import PromptManager

class ValidatorAgent:
    def __init__(self, llm_client: LLMClient, prompt_manager: PromptManager):
        self.llm_client = llm_client
        self.prompt_manager = prompt_manager

    def static_analysis(self, code: str) -> Dict[str, Any]:
        """Perform static analysis on the given code"""
        prompt = self.prompt_manager.get_prompt("static_analysis")
        input_data = {"code": code}
        response = self.llm_client.generate(prompt, input_data)
        return json.loads(response)

    def security_check(self, code: str) -> Dict[str, Any]:
        """Check for security vulnerabilities in the given code"""
        prompt = self.prompt_manager.get_prompt("security_check")
        input_data = {"code": code}
        response = self.llm_client.generate(prompt, input_data)
        return json.loads(response)

    def validate_standards(self, code: str) -> Dict[str, Any]:
        """Validate code against PEP8 and best practices"""
        prompt = self.prompt_manager.get_prompt("validate_standards")
        input_data = {"code": code}
        response = self.llm_client.generate(prompt, input_data)
        return json.loads(response)

    def analyze_complexity(self, code: str) -> Dict[str, Any]:
        """Analyze code complexity"""
        prompt = self.prompt_manager.get_prompt("analyze_complexity")
        input_data = {"code": code}
        response = self.llm_client.generate(prompt, input_data)
        return json.loads(response)

    def fix_issues(self, code: str, issues: List[str]) -> str:
        """Fix identified issues in the code"""
        prompt = self.prompt_manager.get_prompt("fix_issues")
        input_data = {"code": code, "issues": issues}
        response = self.llm_client.generate(prompt, input_data)
        return response