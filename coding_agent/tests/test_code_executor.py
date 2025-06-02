"""
Tests for the Code Executor
"""
import pytest
from unittest.mock import patch, MagicMock
from coding_agent.tools.code_executor import execute_code

def test_execute_code():
    """Test the execute_code function"""
    # Set up the code
    code = "def add(a, b):\n    return a + b\n\na, b = 1, 2\nresult = add(a, b)"

    # Mock subprocess.run
    mock_run = MagicMock()
    mock_run.returncode = 0
    mock_run.stdout = "result = 3"
    mock_run.stderr = ""

    with patch('subprocess.run', return_value=mock_run):
        # Call the function
        result = execute_code(code)

        # Check the result
        assert result["stdout"] == "result = 3"
        assert result["stderr"] == ""
        assert result["returncode"] == 0