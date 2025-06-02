"""
Main entry point for the Coding Agent application
"""
import os
import uvicorn
from api.routes import app
from config.settings import Settings
from core.llm_client import LLMClient
from core.prompt_manager import PromptManager
from agents.programmer_agent import ProgrammerAgent

def main():
    """Run the application"""
    settings = Settings()
    print(f"Starting Coding Agent with settings: {settings.get_settings()}")

    # Initialize LLM client
    api_key = os.getenv("OPENAI_API_KEY", "<your OpenAI API key>")
    llm_client = LLMClient(api_key=api_key, model="gpt-4.1")

    # Initialize prompt manager
    prompt_manager = PromptManager()

    # Initialize programmer agent
    programmer_agent = ProgrammerAgent(llm_client, prompt_manager)

    # Example usage of the agentic workflow
    # This would typically be part of the API endpoint
    issue_description = "Bug: TypeError in the code_executor.py file"
    response = programmer_agent.solve_issue(issue_description)
    print(f"Agent response: {response}")

    # Run the FastAPI application
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()