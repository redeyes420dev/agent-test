"""
Главный файл приложения - Агент автоматизированной разработки кода
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import uvicorn

# Загрузка переменных окружения
load_dotenv()

# Импорт модулей проекта
from coding_agent.api.routes import app as api_router
from coding_agent.api.websocket import app as ws_router
from coding_agent.core.mcp_integration import CodeAgentMcpClient
from coding_agent.config.settings import Settings

# Глобальные переменные
mcp_client = None
settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Жизненный цикл приложения"""
    # Startup
    global mcp_client
    try:
        # Инициализация MCP клиента
        mcp_client = CodeAgentMcpClient(settings.get_settings())
        await mcp_client.initialize_servers()
        print("🚀 MCP серверы инициализированы")
        
        yield
        
    except Exception as e:
        print(f"❌ Ошибка инициализации: {e}")
        yield
    finally:
        # Shutdown
        if mcp_client:
            await mcp_client.cleanup()
        print("🔌 Соединения закрыты")


# Создание приложения FastAPI
app = FastAPI(
    title="Агент автоматизированной разработки кода",
    description="Мульти-агентная система для генерации кода с MCP интеграцией",
    version="1.0.0",
    lifespan=lifespan
)

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
for route in api_router.routes:
    app.add_api_route(route.path, route.endpoint)

for route in ws_router.routes:
    app.add_api_route(route.path, route.endpoint)

# Статические файлы (для React)
if os.path.exists("frontend/build"):
    app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")
    app.mount("/", StaticFiles(directory="frontend/build", html=True), name="react")


@app.get("/health")
async def health_check():
    """Проверка здоровья приложения"""
    return {
        "status": "ok",
        "mcp_servers": len(mcp_client.active_connections) if mcp_client else 0,
        "version": "1.0.0"
    }


@app.get("/api/status")
async def get_status():
    """Статус системы агентов"""
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP клиент не инициализирован")
    
    return {
        "agents_available": True,
        "mcp_servers": {
            name: {"connected": True, "tools": len(conn.tools) if hasattr(conn, 'tools') else 0}
            for name, conn in mcp_client.active_connections.items()
        },
        "model": settings.model
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )