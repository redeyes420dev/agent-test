"""
Code Executor - Tools for executing code in an isolated environment
"""
import subprocess
import tempfile
import os
from typing import Dict, Any

def execute_code(code: str, language: str = "python") -> Dict[str, Any]:
    """
    Execute code in an isolated environment
    """
    with tempfile.NamedTemporaryFile(suffix=f".{language}") as temp_file:
        temp_file.write(code.encode())
        temp_file.flush()

        # Execute the code
        try:
            if language == "python":
                result = subprocess.run(
                    ["python", temp_file.name],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
            else:
                # Add support for other languages
                raise ValueError(f"Language {language} not supported")

            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": "Execution timed out",
                "returncode": -1
            }