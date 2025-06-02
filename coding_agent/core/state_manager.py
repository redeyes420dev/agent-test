"""
State Manager - Manages the state of the agents
"""
import json
from typing import Dict, Any
from pathlib import Path

class StateManager:
    def __init__(self, state_dir: str = "config/state"):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)

    def save_state(self, agent_name: str, state: Dict[str, Any]) -> None:
        """Save the state of an agent"""
        with open(self.state_dir / f"{agent_name}.json", "w") as f:
            json.dump(state, f, indent=2)

    def load_state(self, agent_name: str) -> Dict[str, Any]:
        """Load the state of an agent"""
        state_path = self.state_dir / f"{agent_name}.json"
        if not state_path.exists():
            return {}
        with open(state_path, "r") as f:
            return json.load(f)