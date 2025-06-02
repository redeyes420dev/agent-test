"""
Tests for the CLI interface
"""
import sys
import io
from unittest.mock import patch
from contextlib import redirect_stdout, redirect_stderr
from coding_agent.cli import main

def test_cli_help():
    """Test the CLI help command"""
    # Capture stdout and stderr
    stdout = io.StringIO()
    stderr = io.StringIO()

    # Mock sys.argv to simulate the --help argument
    with patch.object(sys, 'argv', ['cli.py', '--help']):
        with patch('sys.exit'):  # Prevent SystemExit
            with redirect_stdout(stdout), redirect_stderr(stderr):
                # Run the CLI main function
                main()

    # Check that help message was printed
    output = stdout.getvalue()
    assert 'usage:' in output
    assert 'Generate code' in output

def test_cli_generate():
    """Test the CLI generate command"""
    # Capture stdout and stderr
    stdout = io.StringIO()
    stderr = io.StringIO()

    # Mock sys.argv to simulate the generate command
    with patch.object(sys, 'argv', ['cli.py', 'generate', 'Create a simple function']):
        with patch('coding_agent.agents.programmer_agent.ProgrammerAgent.analyze_requirements',
                   return_value={"language": "python", "function_name": "example", "parameters": [], "return_type": "str"}):
            with patch('coding_agent.agents.programmer_agent.ProgrammerAgent.generate_code',
                       return_value="def example():\n    return 'Hello, world!'"):
                with patch('coding_agent.agents.programmer_agent.ProgrammerAgent.create_documentation',
                           return_value="Example function that returns 'Hello, world!'"):
                    with patch('coding_agent.agents.tester_agent.TesterAgent.generate_unit_tests',
                               return_value="def test_example():\n    assert example() == 'Hello, world!'"):
                        with redirect_stdout(stdout), redirect_stderr(stderr):
                            # Run the CLI main function
                            main()

    # Check that code was generated
    output = stdout.getvalue()
    assert 'def example():' in output