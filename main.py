"""
Основной файл для запуска системы кодинг-агентов.

Запускает API Gateway и Frontend на разных портах.
"""

import asyncio
import uvicorn
from multiprocessing import Process
import time
import signal
import sys

def run_api_gateway():
    """Запуск API Gateway."""
    try:
        # Импортируем настройки из api_gateway.py
        import os
        
        # Устанавливаем тестовый ключ если не задан
        if not os.getenv('CODING_AGENT_OPENAI_API_KEY'):
            os.environ['CODING_AGENT_OPENAI_API_KEY'] = 'sk-test-key-demo'
        
        from api_gateway import get_settings
        
        settings = get_settings()
        
        # Создаем FastAPI приложение для API Gateway
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        
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
            return {"status": "healthy", "timestamp": time.time()}
        
        uvicorn.run(
            app,
            host=settings.host,
            port=settings.port,
            log_level=settings.log_level.lower()
        )
        
    except Exception as e:
        print(f"Ошибка при запуске API Gateway: {e}")
        sys.exit(1)

def run_frontend():
    """Запуск Frontend."""
    try:
        # Импортируем код frontend
        from frontend import LLMClient, LLMProvider
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        from fastapi.staticfiles import StaticFiles
        from fastapi.responses import HTMLResponse
        
        app = FastAPI(
            title="Coding Agent Frontend",
            description="Frontend для системы кодинг-агентов",
            version="1.0.0"
        )
        
        # Настройка CORS
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3002", "http://127.0.0.1:3002"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        @app.get("/", response_class=HTMLResponse)
        async def frontend_root():
            return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Coding Agent System</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
                        margin: 0;
                        padding: 40px;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        min-height: 100vh;
                        color: white;
                    }
                    .container {
                        max-width: 1200px;
                        margin: 0 auto;
                        background: rgba(255, 255, 255, 0.1);
                        backdrop-filter: blur(10px);
                        border-radius: 20px;
                        padding: 40px;
                        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                    }
                    h1 {
                        text-align: center;
                        font-size: 2.5em;
                        margin-bottom: 20px;
                        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
                    }
                    .status {
                        text-align: center;
                        font-size: 1.2em;
                        margin-bottom: 30px;
                        padding: 15px;
                        background: rgba(255, 255, 255, 0.2);
                        border-radius: 10px;
                    }
                    .services {
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                        gap: 20px;
                        margin-top: 30px;
                    }
                    .service {
                        background: rgba(255, 255, 255, 0.2);
                        border-radius: 15px;
                        padding: 25px;
                        text-align: center;
                        transition: transform 0.3s ease;
                    }
                    .service:hover {
                        transform: translateY(-5px);
                    }
                    .service h3 {
                        margin-top: 0;
                        font-size: 1.3em;
                    }
                    .service-status {
                        display: inline-block;
                        width: 12px;
                        height: 12px;
                        border-radius: 50%;
                        background: #4CAF50;
                        margin-right: 8px;
                    }
                    a {
                        color: #fff;
                        text-decoration: none;
                        background: rgba(255, 255, 255, 0.2);
                        padding: 10px 20px;
                        border-radius: 25px;
                        transition: background 0.3s ease;
                    }
                    a:hover {
                        background: rgba(255, 255, 255, 0.3);
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🤖 Coding Agent System</h1>
                    <div class="status">
                        <div class="service-status"></div>
                        Frontend Server работает на порту 3002
                    </div>
                    
                    <div class="services">
                        <div class="service">
                            <h3>🚀 API Gateway</h3>
                            <p>Основной API для системы кодинг-агентов</p>
                            <a href="http://localhost:8000" target="_blank">Открыть API (8000)</a>
                        </div>
                        
                        <div class="service">
                            <h3>📊 API Документация</h3>
                            <p>Swagger UI для изучения API</p>
                            <a href="http://localhost:8000/docs" target="_blank">Открыть Docs</a>
                        </div>
                        
                        <div class="service">
                            <h3>🔧 Health Check</h3>
                            <p>Проверка состояния системы</p>
                            <a href="http://localhost:8000/health" target="_blank">Проверить</a>
                        </div>
                        
                        <div class="service">
                            <h3>💻 Frontend</h3>
                            <p>Веб-интерфейс системы</p>
                            <a href="http://localhost:3002" target="_blank">Обновить</a>
                        </div>
                    </div>
                </div>
                
                <script>
                    // Автоматическая проверка статуса каждые 30 секунд
                    setInterval(async () => {
                        try {
                            const response = await fetch('http://localhost:8000/health');
                            if (response.ok) {
                                console.log('API Gateway работает корректно');
                            }
                        } catch (error) {
                            console.warn('Не удается подключиться к API Gateway');
                        }
                    }, 30000);
                </script>
            </body>
            </html>
            """
        
        @app.get("/api/status")
        async def frontend_status():
            return {
                "service": "frontend",
                "status": "running",
                "port": 3002,
                "timestamp": time.time()
            }
        
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=3002,
            log_level="info"
        )
        
    except Exception as e:
        print(f"Ошибка при запуске Frontend: {e}")
        sys.exit(1)

def signal_handler(signum, frame):
    """Обработчик сигналов для корректного завершения."""
    print("\nПолучен сигнал завершения. Останавливаем сервисы...")
    sys.exit(0)

def main():
    """Основная функция запуска."""
    # Регистрируем обработчики сигналов
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("🚀 Запуск системы Coding Agent...")
    print("📡 API Gateway будет доступен на: http://localhost:8000")
    print("🌐 Frontend будет доступен на: http://localhost:3002")
    print("📚 API документация: http://localhost:8000/docs")
    print("\nДля остановки нажмите Ctrl+C")
    
    # Создаем процессы для каждого сервиса
    api_process = Process(target=run_api_gateway, name="API-Gateway")
    frontend_process = Process(target=run_frontend, name="Frontend")
    
    try:
        # Запускаем процессы
        api_process.start()
        time.sleep(2)  # Даем API Gateway время на запуск
        frontend_process.start()
        
        # Ждем завершения процессов
        api_process.join()
        frontend_process.join()
        
    except KeyboardInterrupt:
        print("\nПолучен сигнал остановки...")
        
    finally:
        # Корректно завершаем процессы
        if api_process.is_alive():
            api_process.terminate()
            api_process.join(timeout=5)
            if api_process.is_alive():
                api_process.kill()
        
        if frontend_process.is_alive():
            frontend_process.terminate()
            frontend_process.join(timeout=5)
            if frontend_process.is_alive():
                frontend_process.kill()
        
        print("✅ Все сервисы остановлены")

if __name__ == "__main__":
    main() 