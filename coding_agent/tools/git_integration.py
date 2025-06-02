"""
Git Integration - Tools for interacting with Git
"""
import subprocess
from typing import List

def git_init(repo_path: str) -> None:
    """Initialize a new Git repository"""
    subprocess.run(["git", "init", repo_path], check=True)

def git_add(repo_path: str, files: List[str]) -> None:
    """Add files to the Git index"""
    subprocess.run(["git", "add"] + files, cwd=repo_path, check=True)

def git_commit(repo_path: str, message: str) -> None:
    """Commit changes to the Git repository"""
    subprocess.run(["git", "commit", "-m", message], cwd=repo_path, check=True)

def git_create_branch(repo_path: str, branch_name: str) -> None:
    """Create a new Git branch"""
    subprocess.run(["git", "checkout", "-b", branch_name], cwd=repo_path, check=True)

def git_push(repo_path: str, remote: str, branch: str) -> None:
    """Push changes to a remote repository"""
    subprocess.run(["git", "push", remote, branch], cwd=repo_path, check=True)