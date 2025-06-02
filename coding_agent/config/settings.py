"""
Configuration Settings
"""
import os
from pathlib import Path
from typing import Dict, Any

class Settings:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "your-openai-api-key")
        self.model = os.getenv("LLM_MODEL", "gpt-4.1")
        self.prompts_dir = Path("config/prompts")
        self.state_dir = Path("config/state")
        self.max_context_tokens = int(os.getenv("MAX_CONTEXT_TOKENS", 1000000))

    def get_settings(self) -> Dict[str, Any]:
        """Get all settings as a dictionary"""
        return {
            "api_key": self.api_key,
            "model": self.model,
            "prompts_dir": str(self.prompts_dir),
            "state_dir": str(self.state_dir),
            "max_context_tokens": self.max_context_tokens
        }