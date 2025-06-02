#!/usr/bin/env python3
"""
Тестовый запуск API Gateway
"""

import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Устанавливаем тестовый ключ
os.environ['CODING_AGENT_OPENAI_API_KEY'] = 'sk-test-key-demo'

from api_gateway import get_settings

def main():
    settings = get_settings()
    
    app = FastAPI(
        title="Coding Agent API Gateway",
        description="API Gateway для системы кодинг-агентов",
        version="1.0.0"
    )
    
    # Настройка CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/")
    async def root():
        return {"message": "Coding Agent API Gateway", "status": "running"}
    
    @app.get("/health")
    async def health():
        return {"status": "healthy", "timestamp": 1234567890}
    
    print("🚀 Запуск API Gateway на http://localhost:8000")
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )

if __name__ == "__main__":
    main() 