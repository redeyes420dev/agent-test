"""
CLI interface for the Coding Agent application
"""
import argparse

# Use relative imports
from .agents.programmer_agent import ProgrammerAgent
from .agents.tester_agent import TesterAgent
from .agents.validator_agent import ValidatorAgent
from .core.llm_client import LLMClient
from .core.prompt_manager import PromptManager
from .tools.file_operations import read_file, write_file

def main():
    """Run the CLI interface"""
    parser = argparse.ArgumentParser(description="Coding Agent CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Generate code command
    generate_parser = subparsers.add_parser("generate", help="Generate code")
    generate_parser.add_argument("requirements", help="Requirements for the code")

    # Validate code command
    validate_parser = subparsers.add_parser("validate", help="Validate code")
    validate_parser.add_argument("file_path", help="Path to the code file")

    # Refactor code command
    refactor_parser = subparsers.add_parser("refactor", help="Refactor code")
    refactor_parser.add_argument("file_path", help="Path to the code file")

    # Optimize code command
    optimize_parser = subparsers.add_parser("optimize", help="Optimize code")
    optimize_parser.add_argument("file_path", help="Path to the code file")

    args = parser.parse_args()

    # Initialize components
    llm_client = LLMClient(api_key="your-openai-api-key")
    prompt_manager = PromptManager()
    programmer_agent = ProgrammerAgent(llm_client, prompt_manager)
    tester_agent = TesterAgent(llm_client, prompt_manager)
    validator_agent = ValidatorAgent(llm_client, prompt_manager)

    if args.command == "generate":
        # Generate code
        spec = programmer_agent.analyze_requirements(args.requirements)
        code = programmer_agent.generate_code(spec)
        documentation = programmer_agent.create_documentation(code)
        tests = tester_agent.generate_unit_tests(code)

        print("Generated code:")
        print(code)
        print("\nDocumentation:")
        print(documentation)
        print("\nTests:")
        print(tests)

    elif args.command == "validate":
        # Validate code
        code = read_file(args.file_path)
        analysis = validator_agent.static_analysis(code)
        security = validator_agent.security_check(code)
        standards = validator_agent.validate_standards(code)

        print("Validation results:")
        print(f"Analysis: {analysis}")
        print(f"Security: {security}")
        print(f"Standards: {standards}")

    elif args.command == "refactor":
        # Refactor code
        code = read_file(args.file_path)
        refactored_code = programmer_agent.refactor_code(code)

        print("Refactored code:")
        print(refactored_code)

    elif args.command == "optimize":
        # Optimize code
        code = read_file(args.file_path)
        optimized_code = programmer_agent.optimize_code(code)

        print("Optimized code:")
        print(optimized_code)

if __name__ == "__main__":
    main()