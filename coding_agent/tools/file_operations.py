"""
File Operations - Tools for reading and writing files
"""
import os
from pathlib import Path
from typing import List

def read_file(file_path: str) -> str:
    """Read the contents of a file"""
    with open(file_path, "r") as f:
        return f.read()

def write_file(file_path: str, content: str) -> None:
    """Write content to a file"""
    with open(file_path, "w") as f:
        f.write(content)

def list_files(directory: str) -> List[str]:
    """List files in a directory"""
    return [str(p) for p in Path(directory).glob("**/*") if p.is_file()]

def delete_file(file_path: str) -> None:
    """Delete a file"""
    Path(file_path).unlink()