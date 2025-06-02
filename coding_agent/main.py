"""
Main entry point for the Coding Agent application
"""
import uvicorn
from api.routes import app
from config.settings import Settings

def main():
    """Run the application"""
    settings = Settings()
    print(f"Starting Coding Agent with settings: {settings.get_settings()}")

    # Run the FastAPI application
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()