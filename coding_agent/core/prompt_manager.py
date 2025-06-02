"""
Prompt Manager - Manages prompts for the language model
"""
import json
import os
from typing import Dict, Any
from pathlib import Path

class PromptManager:
    def __init__(self, prompts_dir: str = "config/prompts"):
        self.prompts_dir = Path(prompts_dir)
        self.prompts = self.load_prompts()

        # Add default prompts for testing
        if not self.prompts:
            self.add_default_prompts()

    def load_prompts(self) -> Dict[str, str]:
        """Load prompts from the prompts directory"""
        prompts = {}
        for file_path in self.prompts_dir.glob("*.json"):
            with open(file_path, "r") as f:
                prompt_data = json.load(f)
                prompts[file_path.stem] = prompt_data["prompt"]
        return prompts

    def get_prompt(self, name: str) -> str:
        """Get a prompt by name"""
        if name not in self.prompts:
            raise ValueError(f"Prompt '{name}' not found")
        return self.prompts[name]

    def add_prompt(self, name: str, prompt: str) -> None:
        """Add a new prompt"""
        self.prompts[name] = prompt
        # Save to file
        with open(self.prompts_dir / f"{name}.json", "w") as f:
            json.dump({"prompt": prompt}, f, indent=2)

    def add_default_prompts(self) -> None:
        """Add default prompts for testing"""
        default_prompts = {
            "analyze_requirements": "Analyze the following requirements and return a technical specification in JSON format: {requirements}",
            "generate_code": "Generate code based on the following technical specification: {spec}",
            "create_documentation": "Create documentation for the following code: {code}",
            "generate_tests": "Generate unit tests for the following code: {code}",
            "generate_mocks": "Generate mocks for the following code: {code}",
            "static_analysis": "Perform static analysis on the following code: {code}",
            "security_check": "Perform security analysis on the following code: {code}",
            "validate_standards": "Validate the following code against PEP8 and best practices: {code}",
            "refactor_code": "Refactor the following code to improve quality: {code}",
            "optimize_code": "Optimize the following code for better performance: {code}"
        }

        for name, prompt in default_prompts.items():
            self.prompts[name] = prompt