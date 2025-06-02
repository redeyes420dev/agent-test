"""
LLM клиент для работы с OpenAI GPT-4.1 и структурированным выводом.

Поддерживает JSON Schema валидацию, автоматическое улучшение промптов,
работу с длинным контекстом и интеграцию с различными LLM провайдерами.
"""

import asyncio
import json
import time
import sys
from typing import Any, Dict, List, Optional, Union, Callable, AsyncIterator
from dataclasses import dataclass, field
from enum import Enum
from contextlib import asynccontextmanager

import openai
from openai import AsyncOpenAI
from pydantic import BaseModel, Field, ValidationError
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential, wait_random, retry_if_exception_type
from aiohttp import ClientSession, ClientTimeout, ClientError
from backoff import on_exception, exponential_backoff, full_jitter

from ..config.settings import Settings

class LLMProvider(str, Enum):
    """Поддерживаемые провайдеры LLM."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"
    COHERE = "cohere"
    GOOGLE = "google"
    AZURE = "azure"
    HUGGINGFACE = "huggingface"

class ResponseFormat(str, Enum):
    """Форматы ответов от LLM."""
    TEXT = "text"
    JSON = "json"
    STRUCTURED = "structured"

@dataclass
class LLMMetrics:
    """Метрики использования LLM."""
    total_requests: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0
    average_response_time: float = 0.0
    error_count: int = 0
    last_request_time: Optional[float] = None

@dataclass
class PromptTemplate:
    """Шаблон промпта с метаданными."""
    name: str
    system_prompt: str
    user_prompt_template: str
    response_format: ResponseFormat = ResponseFormat.TEXT
    json_schema: Optional[Dict[str, Any]] = None
    examples: List[Dict[str, str]] = field(default_factory=list)
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None

class StructuredResponse(BaseModel):
    """Структурированный ответ от LLM."""
    content: str = Field(description="Основное содержимое ответа")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Метаданные ответа")
    confidence: Optional[float] = Field(default=None, description="Уверенность модели в ответе")
    reasoning: Optional[str] = Field(default=None, description="Обоснование ответа")

class CodeGenerationRequest(BaseModel):
    """Запрос на генерацию кода."""
    requirements: str = Field(description="Требования к коду")
    language: str = Field(description="Язык программирования")
    framework: Optional[str] = Field(default=None, description="Фреймворк или библиотека")
    style_guide: Optional[str] = Field(default=None, description="Руководство по стилю")
    include_comments: bool = Field(default=True, description="Включить комментарии")
    include_docstrings: bool = Field(default=True, description="Включить docstrings")
    complexity_level: str = Field(default="intermediate", description="Уровень сложности")

class CodeResponse(BaseModel):
    """Ответ с сгенерированным кодом."""
    code: str = Field(description="Сгенерированный код")
    explanation: str = Field(description="Объяснение кода")
    dependencies: List[str] = Field(default_factory=list, description="Зависимости")
    usage_example: Optional[str] = Field(default=None, description="Пример использования")
    complexity_analysis: Dict[str, Any] = Field(default_factory=dict, description="Анализ сложности")

class LLMClient:
    """
    Клиент для работы с Large Language Models.

    Поддерживает OpenAI GPT-4.1, структурированный вывод, автоматическое улучшение промптов
    и интеграцию с различными провайдерами LLM.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4-1106-preview",
        provider: LLMProvider = LLMProvider.OPENAI,
        base_url: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 4000,
        timeout: int = 60
    ):
        """
        Инициализация LLM клиента.

        Args:
            api_key: API ключ для провайдера
            model: Название модели
            provider: Провайдер LLM
            base_url: Базовый URL для API (опционально)
            temperature: Температура для генерации
            max_tokens: Максимальное количество токенов
            timeout: Таймаут запросов в секундах
        """
        self.api_key = api_key
        self.model = model
        self.provider = provider
        self.base_url = base_url
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout

        # Инициализация клиентов
        self._init_clients()

        # Метрики и кэш
        self.metrics = LLMMetrics()
        self._response_cache: Dict[str, Any] = {}
        self._prompt_templates: Dict[str, PromptTemplate] = {}

        logger.info(f"Инициализирован LLM клиент: {provider.value}/{model}")

    def _init_clients(self):
        """Инициализация клиентов для разных провайдеров."""
        if self.provider == LLMProvider.OPENAI:
            self.client = AsyncOpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=ClientTimeout(total=self.timeout)
            )
            self.client_type = "openai"
        elif self.provider == LLMProvider.ANTHROPIC:
            self.client = None  # Will be initialized when needed
            self.client_type = "anthropic"
        elif self.provider == LLMProvider.COHERE:
            self.client = None  # Will be initialized when needed
            self.client_type = "cohere"
        elif self.provider == LLMProvider.GOOGLE:
            self.client = None  # Will be initialized when needed
            self.client_type = "google"
        elif self.provider == LLMProvider.AZURE:
            self.client = None  # Will be initialized when needed
            self.client_type = "azure"
        elif self.provider == LLMProvider.HUGGINGFACE:
            self.client = None  # Will be initialized when needed
            self.client_type = "huggingface"
        elif self.provider == LLMProvider.LOCAL:
            self.client = None  # Will be initialized when needed
            self.client_type = "local"
        else:
            raise ValueError(f"Провайдер {self.provider} не поддерживается")

    def register_prompt_template(self, template: PromptTemplate):
        """Регистрация шаблона промпта."""
        self._prompt_templates[template.name] = template
        logger.debug(f"Зарегистрирован шаблон промпта: {template.name}")

    async def load_prompt_templates(self, directory: str):
        """
        Загрузка шаблонов промптов из директории.

        Args:
            directory: Путь к директории с файлами шаблонов
        """
        import os
        import json
        import yaml

        if not os.path.isdir(directory):
            logger.warning(f"Директория с шаблонами промптов не найдена: {directory}")
            return

        for filename in os.listdir(directory):
            if filename.endswith(('.json', '.yaml', '.yml')):
                file_path = os.path.join(directory, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        if filename.endswith('.json'):
                            template_data = json.load(f)
                        else:
                            template_data = yaml.safe_load(f)

                        # Convert to PromptTemplate
                        template = PromptTemplate(
                            name=template_data['name'],
                            system_prompt=template_data['system_prompt'],
                            user_prompt_template=template_data['user_prompt_template'],
                            response_format=ResponseFormat(template_data.get('response_format', 'text')),
                            json_schema=template_data.get('json_schema'),
                            examples=template_data.get('examples', []),
                            temperature=template_data.get('temperature'),
                            max_tokens=template_data.get('max_tokens')
                        )

                        self.register_prompt_template(template)
                        logger.info(f"Загружен шаблон промпта из файла: {filename}")
                except Exception as e:
                    logger.error(f"Ошибка при загрузке шаблона из файла {filename}: {e}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> Union[str, AsyncIterator[str]]:
        """
        Генерация текста с использованием LLM.

        Args:
            prompt: Пользовательский промпт
            system_prompt: Системный промпт
            temperature: Температура генерации
            max_tokens: Максимальное количество токенов
            stream: Включить потоковый режим (streaming)
            **kwargs: Дополнительные параметры

        Returns:
            Union[str, AsyncIterator[str]]: Сгенерированный текст или итератор для потокового режима
        """
        start_time = time.time()

        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            if stream:
                return self._stream_response(messages, temperature, max_tokens, **kwargs)
            else:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature or self.temperature,
                    max_tokens=max_tokens or self.max_tokens,
                    **kwargs
                )

                content = response.choices[0].message.content

                # Обновление метрик
                self._update_metrics(response, time.time() - start_time)

                return content

        except Exception as e:
            self.metrics.error_count += 1
            logger.error(f"Ошибка при генерации текста: {e}")
            raise

    async def _stream_response(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncIterator[str]:
        """
        Потоковая генерация текста.

        Args:
            messages: Сообщения для отправки в LLM
            temperature: Температура генерации
            max_tokens: Максимальное количество токенов
            **kwargs: Дополнительные параметры

        Returns:
            AsyncIterator[str]: Итератор для потокового режима
        """
        try:
            async with self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
                stream=True,
                **kwargs
            ) as response:
                full_content = ""
                async for chunk in response:
                    if hasattr(chunk.choices[0].delta, 'content'):
                        content = chunk.choices[0].delta.content
                        full_content += content
                        yield content

                # Обновление метрик после получения полного ответа
                self._update_metrics(response, time.time() - self.metrics.last_request_time)
        except Exception as e:
            self.metrics.error_count += 1
            logger.error(f"Ошибка при потоковой генерации текста: {e}")
            raise

    async def generate_structured(
        self,
        prompt: str,
        response_schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Генерация структурированного ответа с JSON Schema валидацией.

        Args:
            prompt: Пользовательский промпт
            response_schema: JSON Schema для валидации ответа
            system_prompt: Системный промпт
            temperature: Температура генерации
            **kwargs: Дополнительные параметры

        Returns:
            Dict[str, Any]: Структурированный ответ
        """
        start_time = time.time()

        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "structured_response",
                        "strict": True,
                        "schema": response_schema
                    }
                },
                **kwargs
            )

            content = response.choices[0].message.content
            structured_data = json.loads(content)

            # Обновление метрик
            self._update_metrics(response, time.time() - start_time)

            return structured_data

        except Exception as e:
            self.metrics.error_count += 1
            logger.error(f"Ошибка при генерации структурированного ответа: {e}")
            raise

    async def generate_code(
        self,
        request: CodeGenerationRequest,
        template_name: Optional[str] = None
    ) -> CodeResponse:
        """
        Генерация кода с использованием специализированного промпта.

        Args:
            request: Запрос на генерацию кода
            template_name: Имя шаблона промпта

        Returns:
            CodeResponse: Ответ с сгенерированным кодом
        """
        # Использование шаблона промпта если указан
        if template_name and template_name in self._prompt_templates:
            template = self._prompt_templates[template_name]
            system_prompt = template.system_prompt
            user_prompt = template.user_prompt_template.format(**request.dict())
        else:
            system_prompt = self._get_default_code_system_prompt(request.language)
            user_prompt = self._format_code_prompt(request)

        # JSON Schema для структурированного ответа
        response_schema = {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Сгенерированный код"},
                "explanation": {"type": "string", "description": "Объяснение кода"},
                "dependencies": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Список зависимостей"
                },
                "usage_example": {"type": "string", "description": "Пример использования"},
                "complexity_analysis": {
                    "type": "object",
                    "properties": {
                        "time_complexity": {"type": "string"},
                        "space_complexity": {"type": "string"},
                        "maintainability": {"type": "number", "minimum": 1, "maximum": 10}
                    },
                    "required": ["time_complexity", "space_complexity", "maintainability"]
                }
            },
            "required": ["code", "explanation", "dependencies", "complexity_analysis"],
            "additionalProperties": False
        }

        result = await self.generate_structured(
            prompt=user_prompt,
            response_schema=response_schema,
            system_prompt=system_prompt
        )

        return CodeResponse(**result)

    async def improve_prompt(
        self,
        original_prompt: str,
        desired_outcome: str,
        performance_feedback: Optional[str] = None
    ) -> str:
        """
        Автоматическое улучшение промпта на основе обратной связи.

        Args:
            original_prompt: Исходный промпт
            desired_outcome: Желаемый результат
            performance_feedback: Обратная связь о производительности

        Returns:
            str: Улучшенный промпт
        """
        improvement_prompt = f"""
        Проанализируй следующий промпт и улучши его для получения более качественных результатов:

        Исходный промпт:
        {original_prompt}

        Желаемый результат:
        {desired_outcome}

        Обратная связь о производительности:
        {performance_feedback or "Не предоставлена"}

        Принципы улучшения промптов для GPT-4.1:
        1. Четкость и конкретность инструкций
        2. Структурированный формат с XML-разметкой
        3. Принципы настойчивости, использования инструментов и планирования
        4. Контекстно-зависимые инструкции
        5. Примеры для демонстрации ожидаемого поведения

        Предоставь улучшенную версию промпта:
        """

        return await self.generate_text(improvement_prompt)

    def _get_default_code_system_prompt(self, language: str) -> str:
        """Получение системного промпта по умолчанию для генерации кода."""
        return f"""
        <agent_role>
        Вы - эксперт-программист со специализацией на языке {language}. Ваша задача - генерировать высококачественный,
        чистый и хорошо документированный код в соответствии с лучшими практиками и стандартами.
        </agent_role>

        <instructions>
        1. ВСЕГДА следуйте принципам чистого кода и SOLID
        2. Включайте подробные комментарии и docstrings
        3. Обеспечивайте обработку ошибок где это необходимо
        4. Используйте описательные имена переменных и функций
        5. Структурируйте код для максимальной читаемости
        6. Предоставляйте анализ сложности и зависимостей
        </instructions>

        <output_format>
        Ответ должен быть в структурированном JSON формате с полями:
        - code: исполняемый код
        - explanation: детальное объяснение
        - dependencies: список необходимых зависимостей
        - usage_example: пример использования
        - complexity_analysis: анализ временной и пространственной сложности
        </output_format>

        <quality_standards>
        - Код должен быть готов к продакшену
        - Все функции должны иметь type hints (для Python)
        - Обязательна обработка edge cases
        - Код должен быть тестируемым
        </quality_standards>
        """

    def _format_code_prompt(self, request: CodeGenerationRequest) -> str:
        """Форматирование промпта для генерации кода."""
        prompt = f"""
        Сгенерируй код на языке {request.language} для следующих требований:

        Требования: {request.requirements}
        """

        if request.framework:
            prompt += f"\nФреймворк/библиотека: {request.framework}"

        if request.style_guide:
            prompt += f"\nРуководство по стилю: {request.style_guide}"

        prompt += f"""

        Дополнительные требования:
        - Включить комментарии: {request.include_comments}
        - Включить docstrings: {request.include_docstrings}
        - Уровень сложности: {request.complexity_level}

        Убедись, что код соответствует всем требованиям и лучшим практикам для {request.language}.
        """

        return prompt

    def _update_metrics(self, response: Any, response_time: float):
        """Обновление метрик использования."""
        self.metrics.total_requests += 1
        self.metrics.last_request_time = time.time()

        if hasattr(response, 'usage'):
            tokens = response.usage.total_tokens
            self.metrics.total_tokens += tokens

            # Примерная стоимость для GPT-4
            cost_per_token = 0.00003  # $0.03 per 1K tokens
            self.metrics.total_cost += tokens * cost_per_token

        # Обновление среднего времени ответа
        total_time = self.metrics.average_response_time * (self.metrics.total_requests - 1)
        self.metrics.average_response_time = (total_time + response_time) / self.metrics.total_requests

    def get_metrics(self) -> Dict[str, Any]:
        """Получение метрик использования."""
        return {
            "total_requests": self.metrics.total_requests,
            "total_tokens": self.metrics.total_tokens,
            "total_cost_usd": round(self.metrics.total_cost, 2),
            "average_response_time": round(self.metrics.average_response_time, 2),
            "error_count": self.metrics.error_count
        }