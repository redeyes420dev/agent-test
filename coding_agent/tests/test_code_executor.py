"""
Tests for the Code Executor
"""
import pytest
from tools.code_executor import execute_code

def test_execute_code():
    """Test the execute_code function"""
    # Set up the code
    code = "def add(a, b):\n    return a + b\n\na, b = 1, 2\nresult = add(a, b)"

    # Call the function
    result = execute_code(code)

    # Check the result
    assert "result = 3" in result