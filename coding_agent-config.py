"""
Настройки конфигурации для агента разработки
"""

import os
from typing import List, Dict, Any
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Основные настройки приложения"""
    
    # OpenAI API
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = "gpt-4.1-mini-2025-04-14"
    max_tokens: int = 32768
    
    # Anthropic API
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # GitHub API
    github_token: str = os.getenv("GITHUB_TOKEN", "")
    
    # Bright Data API
    brightdata_token: str = os.getenv("BRIGHTDATA_TOKEN", "")
    
    # База данных
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./coding_agent.db")
    
    # Безопасность
    encryption_key: str = os.getenv("ENCRYPTION_KEY", "")
    jwt_secret: str = os.getenv("JWT_SECRET", "your-super-secret-key")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Git настройки
    git_workspace: str = os.getenv("GIT_WORKSPACE", "./repos")
    max_repo_size: str = "500MB"
    allowed_domains: List[str] = ["github.com", "gitlab.com", "bitbucket.org"]
    
    # MCP серверы конфигурация
    mcp_servers: List[Dict[str, Any]] = [
        {
            "name": "sandbox",
            "command": "python",
            "args": ["-m", "mcp_servers.sandbox"],
            "env": {"SANDBOX_MODE": "secure"}
        },
        {
            "name": "testing",
            "command": "node",
            "args": ["mcp_servers/testing-server.js"],
            "env": {}
        },
        {
            "name": "documentation",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-docs"],
            "env": {}
        },
        {
            "name": "github",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN", "")}
        },
        {
            "name": "brightdata",
            "command": "npx",
            "args": ["-y", "@brightdata/mcp"],
            "env": {"API_TOKEN": os.getenv("BRIGHTDATA_TOKEN", "")}
        }
    ]
    
    # Настройки агентов
    max_iterations: int = 10
    debug_mode: bool = os.getenv("DEBUG_MODE", "false").lower() == "true"
    context_window_size: int = 1000000
    
    # Веб-сервер
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Мониторинг
    enable_metrics: bool = True
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Глобальный экземпляр настроек
settings = Settings()


# MCP серверы для различных задач
MCP_SERVERS_CONFIG = {
    "code_execution": {
        "sandbox": {
            "name": "sandbox",
            "command": "python",
            "args": ["-m", "mcp_servers.sandbox"],
            "env": {"SANDBOX_MODE": "secure"},
            "tools": ["python_execute", "js_eval", "secure_container_run"]
        }
    },
    "quality_control": {
        "linting": {
            "name": "code_quality",
            "command": "python",
            "args": ["-m", "mcp_servers.quality"],
            "env": {},
            "tools": ["pylint", "black", "mypy", "eslint", "prettier"]
        }
    },
    "documentation": {
        "docs": {
            "name": "documentation",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-docs"],
            "env": {},
            "tools": ["search_pypi", "search_npm", "get_docs"]
        }
    },
    "git_integration": {
        "github": {
            "name": "github",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": settings.github_token},
            "tools": ["create_repo", "search_code", "create_pr", "get_issues"]
        }
    },
    "web_research": {
        "brightdata": {
            "name": "brightdata",
            "command": "npx",
            "args": ["-y", "@brightdata/mcp"],
            "env": {"API_TOKEN": settings.brightdata_token},
            "tools": ["web_search", "scrape_page", "get_trends"]
        }
    }
}


# Промпты для агентов
SYSTEM_PROMPTS = {
    "programmer": """
    <Role>
    Ты - экспертный программист с доступом к современным инструментам разработки через MCP.
    </Role>
    
    <Constraints>
    - Всегда используй GPT-4.1-mini модель для генерации кода
    - Следуй принципам настойчивости, использования инструментов и планирования
    - Используй MCP-серверы для валидации и тестирования кода
    - Применяй best practices для выбранного языка программирования
    </Constraints>
    
    <Tools>
    - MCP Sandbox для безопасного выполнения кода
    - MCP Documentation для поиска актуальной документации
    - MCP Quality для проверки стиля и качества кода
    - MCP GitHub для работы с репозиториями
    </Tools>
    """,
    
    "tester": """
    <Role>
    Ты - специалист по тестированию, создающий комплексные тесты для кода.
    </Role>
    
    <Constraints>
    - Создавай unit-тесты, интеграционные тесты и тесты безопасности
    - Используй соответствующие фреймворки (pytest, jest, mocha)
    - Обеспечивай высокое покрытие кода тестами
    </Constraints>
    """,
    
    "validator": """
    <Role>
    Ты - аналитик качества кода, проверяющий соответствие стандартам.
    </Role>
    
    <Constraints>
    - Анализируй код на соответствие стандартам (PEP8, ESLint)
    - Проверяй безопасность и производительность
    - Предлагай улучшения и рефакторинг
    </Constraints>
    """
}