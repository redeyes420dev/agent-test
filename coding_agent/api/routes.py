"""
API Routes - Define the API endpoints
"""
import os
import subprocess
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any
from coding_agent.agents.programmer_agent import ProgrammerAgent
from coding_agent.agents.tester_agent import TesterAgent
from coding_agent.agents.validator_agent import ValidatorAgent
from coding_agent.core.llm_client import LLMClient
from coding_agent.core.prompt_manager import PromptManager
from coding_agent.core.state_manager import StateManager

app = FastAPI()

# Initialize components
api_key = os.getenv("OPENAI_API_KEY", "your-openai-api-key")
llm_client = LLMClient(api_key=api_key, model="gpt-4.1")
prompt_manager = PromptManager()
state_manager = StateManager()

# Initialize agents
programmer_agent = ProgrammerAgent(llm_client, prompt_manager)
tester_agent = TesterAgent(llm_client, prompt_manager)
validator_agent = ValidatorAgent(llm_client, prompt_manager)

class CodeRequest(BaseModel):
    requirements: str

class CodeResponse(BaseModel):
    code: str
    documentation: str
    tests: str

class IssueRequest(BaseModel):
    description: str

class IssueResponse(BaseModel):
    solution: Dict[str, Any]

class PatchRequest(BaseModel):
    patch: str

class PatchResponse(BaseModel):
    result: str

@app.post("/generate_code", response_model=CodeResponse)
def generate_code(request: CodeRequest) -> CodeResponse:
    """Generate code based on requirements"""
    try:
        # Analyze requirements
        spec = programmer_agent.analyze_requirements(request.requirements)

        # Generate code
        code = programmer_agent.generate_code(spec)

        # Create documentation
        documentation = programmer_agent.create_documentation(code)

        # Generate tests
        tests = tester_agent.generate_unit_tests(code)

        return CodeResponse(code=code, documentation=documentation, tests=tests)
    except Exception as e:
        print(f"Error in generate_code: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/validate_code")
def validate_code(code: Dict[str, Any]) -> Dict[str, Any]:
    """Validate code quality"""
    try:
        code_str = code.get("code", "")

        # Perform static analysis
        analysis = validator_agent.static_analysis(code_str)

        # Check for security issues
        security = validator_agent.security_check(code_str)

        # Validate against standards
        standards = validator_agent.validate_standards(code_str)

        return {
            "analysis": analysis,
            "security": security,
            "standards": standards
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/refactor_code")
def refactor_code(code: str) -> str:
    """Refactor code to improve quality"""
    try:
        refactored_code = programmer_agent.refactor_code(code)
        return refactored_code
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/optimize_code")
def optimize_code(code: str) -> str:
    """Optimize code for better performance"""
    try:
        optimized_code = programmer_agent.optimize_code(code)
        return optimized_code
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/solve_issue", response_model=IssueResponse)
def solve_issue(request: IssueRequest) -> IssueResponse:
    """Solve an issue using the agentic workflow with tools"""
    try:
        # Use the agentic workflow to solve the issue
        solution = programmer_agent.solve_issue(request.description)
        return IssueResponse(solution=solution)
    except Exception as e:
        print(f"Error in solve_issue: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/apply_patch", response_model=PatchResponse)
def apply_patch(request: PatchRequest) -> PatchResponse:
    """Apply a patch to the codebase"""
    try:
        # Execute the apply_patch script with the provided patch
        process = subprocess.Popen(
            ["python", "coding_agent/tools/apply_patch.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Send the patch to the script
        stdout, stderr = process.communicate(request.patch)

        # Check if there were any errors
        if process.returncode != 0 or "Done!" not in stdout:
            error_msg = f"Patch application failed: {stderr}"
            print(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)

        return PatchResponse(result="Patch applied successfully")
    except Exception as e:
        print(f"Error in apply_patch: {e}")
        raise HTTPException(status_code=500, detail=str(e))