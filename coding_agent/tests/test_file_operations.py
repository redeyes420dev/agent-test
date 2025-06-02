"""
Tests for the File Operations
"""
import pytest
import os
import tempfile
from coding_agent.tools.file_operations import read_file, write_file

def test_read_write_file():
    """Test the read_file and write_file functions"""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp_path = temp.name

    try:
        # Write to the file
        content = "Hello, world!"
        write_file(temp_path, content)

        # Read from the file
        result = read_file(temp_path)

        # Check the result
        assert result == content
    finally:
        # Clean up
        os.unlink(temp_path)