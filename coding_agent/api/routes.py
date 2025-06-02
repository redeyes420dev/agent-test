"""
API Routes - Define the API endpoints
"""
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any
from agents.programmer_agent import ProgrammerAgent
from agents.tester_agent import TesterAgent
from agents.validator_agent import ValidatorAgent
from core.llm_client import LLMClient
from core.prompt_manager import PromptManager
from core.state_manager import StateManager

app = FastAPI()

# Initialize components
llm_client = LLMClient(api_key="your-openai-api-key")
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
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/validate_code")
def validate_code(code: str) -> Dict[str, Any]:
    """Validate code quality"""
    try:
        # Perform static analysis
        analysis = validator_agent.static_analysis(code)

        # Check for security issues
        security = validator_agent.security_check(code)

        # Validate against standards
        standards = validator_agent.validate_standards(code)

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