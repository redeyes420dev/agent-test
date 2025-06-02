"""
Prompt Manager - Manages prompts for the language model
"""
import json
from typing import Dict, Any
from pathlib import Path

class PromptManager:
    def __init__(self, prompts_dir: str = "config/prompts"):
        self.prompts_dir = Path(prompts_dir)
        self.prompts = self.load_prompts()

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