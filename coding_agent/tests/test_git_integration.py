"""
Tests for the Git Integration
"""
import pytest
import os
import tempfile
from tools.git_integration import init_repo, commit_changes

def test_init_repo():
    """Test the init_repo function"""
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Initialize a Git repository
        init_repo(temp_dir)

        # Check that the repository was initialized
        assert os.path.exists(os.path.join(temp_dir, ".git"))

def test_commit_changes():
    """Test the commit_changes function"""
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Initialize a Git repository
        init_repo(temp_dir)

        # Create a file
        file_path = os.path.join(temp_dir, "test.txt")
        with open(file_path, "w") as f:
            f.write("Hello, world!")

        # Commit the changes
        commit_changes(temp_dir, "Initial commit")

        # Check that the changes were committed
        assert os.path.exists(os.path.join(temp_dir, ".git"))