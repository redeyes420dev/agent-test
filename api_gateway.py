"""
Настройки приложения для системы кодинг-агентов.

Использует Pydantic Settings для управления конфигурацией через переменные окружения
и файлы конфигурации. Поддерживает различные профили для разработки и продакшена.
"""

import os
import sys
import secrets
import json
from typing import List, Optional, Dict, Any, Union, Tuple
from pydantic import Field, validator, ValidationError
from pydantic_settings import BaseSettings
from pathlib import Path
import yaml

class Settings(BaseSettings):
    """
    Основные настройки приложения.

    Все настройки могут быть переопределены через переменные окружения
    с префиксом CODING_AGENT_ (например, CODING_AGENT_OPENAI_API_KEY).
    Поддерживает загрузку из файлов конфигурации в формате YAML/JSON.
    """

    # Основные настройки приложения
    app_name: str = Field(default="Coding Agent System", description="Название приложения")
    version: str = Field(default="1.0.0", description="Версия приложения")
    debug: bool = Field(default=False, description="Режим отладки")
    host: str = Field(default="127.0.0.1", description="Хост для запуска сервера")
    port: int = Field(default=8000, description="Порт для запуска сервера")

    # OpenAI настройки
    openai_api_key: str = Field(..., description="API ключ OpenAI")
    openai_model: str = Field(default="gpt-4-1106-preview", description="Модель OpenAI для использования")
    openai_api_base: Optional[str] = Field(default=None, description="Базовый URL для OpenAI API")
    llm_temperature: float = Field(default=0.2, description="Температура для LLM")
    llm_max_tokens: int = Field(default=4000, description="Максимальное количество токенов")

    # Настройки базы данных и кэша
    database_url: str = Field(default="sqlite+aiosqlite:///./coding_agent.db", description="URL базы данных")
    redis_url: str = Field(default="redis://localhost:6379/0", description="URL Redis сервера")

    # Настройки безопасности
    secret_key: str = Field(default_factory=lambda: secrets.token_hex(32), description="Секретный ключ для JWT")
    access_token_expire_minutes: int = Field(default=30, description="Время жизни токена доступа в минутах")
    allowed_hosts: List[str] = Field(default=["localhost", "127.0.0.1"], description="Разрешенные хосты")
    cors_origins: List[str] = Field(default=["*"], description="Разрешенные источники для CORS")
    api_key_required: bool = Field(default=False, description="Требовать API ключ для доступа")
    api_keys: List[str] = Field(default_factory=list, description="Список разрешенных API ключей")

    # Настройки Docker
    docker_socket: str = Field(default="unix:///var/run/docker.sock", description="Путь к Docker socket")
    default_docker_image: str = Field(default="python:3.11-slim", description="Docker образ по умолчанию")
    docker_network: str = Field(default="coding_agent_network", description="Docker сеть")
    container_timeout: int = Field(default=300, description="Таймаут выполнения в контейнере (секунды)")

    # Настройки Git
    default_git_branch: str = Field(default="main", description="Ветка Git по умолчанию")
    git_commit_author_name: str = Field(default="Coding Agent", description="Имя автора коммитов")
    git_commit_author_email: str = Field(default="agent@codingagent.dev", description="Email автора коммитов")

    # Настройки файловой системы
    workspace_dir: Path = Field(default=Path("./workspace"), description="Рабочая директория")
    max_file_size: int = Field(default=10 * 1024 * 1024, description="Максимальный размер файла (байты)")
    allowed_file_extensions: List[str] = Field(
        default=[".py", ".js", ".ts", ".java", ".cpp", ".c", ".go", ".rs", ".md", ".txt", ".json", ".yaml", ".yml"],
        description="Разрешенные расширения файлов"
    )

    # Настройки агентов
    max_iterations: int = Field(default=10, description="Максимальное количество итераций агента")
    agent_timeout: int = Field(default=600, description="Таймаут выполнения агента (секунды)")
    enable_parallel_agents: bool = Field(default=True, description="Включить параллельное выполнение агентов")
    max_concurrent_agents: int = Field(default=5, description="Максимальное количество параллельных агентов")

    # Настройки промптов
    prompt_templates_dir: Path = Field(default=Path("./coding_agent/config/prompts"), description="Директория с шаблонами промптов")
    enable_prompt_optimization: bool = Field(default=True, description="Включить оптимизацию промптов")
    prompt_cache_size: int = Field(default=100, description="Размер кэша для промптов")

    # Настройки тестирования
    test_framework: str = Field(default="pytest", description="Фреймворк для тестирования")
    test_timeout: int = Field(default=60, description="Таймаут выполнения тестов (секунды)")
    enable_coverage: bool = Field(default=True, description="Включить анализ покрытия кода")
    test_retry_count: int = Field(default=2, description="Количество попыток для перезапуска тестов")

    # Настройки валидации кода
    enable_static_analysis: bool = Field(default=True, description="Включить статический анализ")
    linting_tools: List[str] = Field(default=["flake8", "pylint", "mypy"], description="Инструменты для линтинга")
    code_quality_threshold: float = Field(default=8.0, description="Пороговое значение качества кода")

    # Настройки мониторинга
    enable_metrics: bool = Field(default=True, description="Включить метрики")
    metrics_port: int = Field(default=9090, description="Порт для метрик Prometheus")
    log_level: str = Field(default="INFO", description="Уровень логирования")
    log_retention_days: int = Field(default=7, description="Количество дней хранения логов")

    # Настройки WebSocket
    websocket_ping_interval: int = Field(default=20, description="Интервал ping для WebSocket (секунды)")
    websocket_ping_timeout: int = Field(default=20, description="Таймаут ping для WebSocket (секунды)")
    max_websocket_connections: int = Field(default=100, description="Максимальное количество WebSocket подключений")

    # MCP настройки
    mcp_enabled: bool = Field(default=True, description="Включить поддержку MCP")
    mcp_servers: Dict[str, Dict[str, Any]] = Field(
        default={
            "filesystem": {
                "command": "npx",
                "args": ["@modelcontextprotocol/server-filesystem", "./workspace"],
                "env": {}
            }
        },
        description="Конфигурация MCP серверов"
    )

    # Настройки VS Code расширения
    vscode_extension_enabled: bool = Field(default=True, description="Включить интеграцию с VS Code")
    vscode_extension_port: int = Field(default=8001, description="Порт для VS Code расширения")

    # Настройки API
    api_rate_limit: int = Field(default=100, description="Лимит запросов к API в минуту")
    api_rate_limit_burst: int = Field(default=50, description="Бurst размер для лимита запросов")

    # Настройки healthcheck
    healthcheck_enabled: bool = Field(default=True, description="Включить healthcheck endpoint")
    healthcheck_interval: int = Field(default=60, description="Интервал проверки здоровья (секунды)")

    # Настройки резервного копирования
    enable_backups: bool = Field(default=False, description="Включить автоматическое резервное копирование")
    backup_interval: int = Field(default=24 * 60, description="Интервал резервного копирования (в минутах)")
    backup_retention: int = Field(default=7, description="Количество дней хранения резервных копий")

    @validator("workspace_dir", pre=True)
    def create_workspace_dir(cls, v):
        """Создает рабочую директорию если она не существует."""
        workspace_path = Path(v)
        workspace_path.mkdir(parents=True, exist_ok=True)
        return workspace_path

    @validator("openai_api_key")
    def validate_openai_api_key(cls, v):
        """Проверяет что API ключ OpenAI задан."""
        if not v or v == "your-openai-api-key" or v.isspace():
            raise ValueError("OpenAI API ключ должен быть задан и не должен быть пустым")
        return v

    @validator("llm_temperature")
    def validate_temperature(cls, v):
        """Проверяет что температура в допустимом диапазоне."""
        if not 0.0 <= v <= 2.0:
            raise ValueError("Температура должна быть между 0.0 и 2.0")
        return v

    @validator("log_level")
    def validate_log_level(cls, v):
        """Проверяет корректность уровня логирования."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Уровень логирования должен быть одним из: {valid_levels}")
        return v.upper()

    @validator("api_keys")
    def validate_api_keys(cls, v):
        """Проверяет что API ключи не пустые и не содержат пробелы."""
        if not v:
            return v

        for key in v:
            if not key or key.isspace():
                raise ValueError("API ключи не должны быть пустыми или содержать только пробелы")
        return v

    class Config:
        env_prefix = "CODING_AGENT_"
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @classmethod
    def from_yaml(cls, file_path: Union[str, Path]):
        """Загрузка настроек из YAML файла."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return cls(**data)

    @classmethod
    def from_json(cls, file_path: Union[str, Path]):
        """Загрузка настроек из JSON файла."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(**data)

class DevelopmentSettings(Settings):
    """Настройки для разработки."""
    debug: bool = True
    log_level: str = "DEBUG"
    host: str = "127.0.0.1"
    port: int = 8000

class ProductionSettings(Settings):
    """Настройки для продакшена."""
    debug: bool = False
    log_level: str = "INFO"
    host: str = "0.0.0.0"
    port: int = 8000

class TestSettings(Settings):
    """Настройки для тестирования."""
    debug: bool = True
    database_url: str = "sqlite+aiosqlite:///./test_coding_agent.db"
    redis_url: str = "redis://localhost:6379/1"
    log_level: str = "DEBUG"

def get_settings() -> Settings:
    """
    Получение настроек в зависимости от окружения.

    Returns:
        Settings: Объект настроек для текущего окружения
    """
    environment = os.getenv("ENVIRONMENT", "development").lower()

    if environment == "production":
        return ProductionSettings()
    elif environment == "test":
        return TestSettings()
    else:
        return DevelopmentSettings()

# Экспорт основного класса настроек
__all__ = ["Settings", "get_settings", "DevelopmentSettings", "ProductionSettings", "TestSettings"]