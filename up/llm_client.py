"""
LLM клиент для работы с GPT-4.1-mini и другими моделями
"""

import os
import logging
from typing import Dict, Any, Optional, List
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from pydantic import BaseModel

# Настройка логирования
logger = logging.getLogger("llm_client")


class CodeResponse(BaseModel):
    """Модель ответа для генерации кода"""
    code: str
    language: str
    dependencies: List[str] = []
    explanation: str = ""
    tests: str = ""
    documentation: str = ""


class LLMClient:
    """Клиент для работы с различными LLM провайдерами"""
    
    def __init__(self, api_key: str, provider: str = "openai"):
        self.provider = provider
        self.api_key = api_key
        
        if provider == "openai":
            self.client = AsyncOpenAI(api_key=api_key)
            self.model = "gpt-4.1-mini-2025-04-14"
        elif provider == "anthropic":
            self.client = AsyncAnthropic(api_key=api_key)
            self.model = "claude-3-5-sonnet-20241022"
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    async def generate_code(
        self, 
        prompt: str,
        language: str = "python",
        response_model: Optional[BaseModel] = None,
        **kwargs
    ) -> CodeResponse:
        """Генерация кода с использованием LLM"""
        
        system_prompt = self._build_system_prompt(language)
        user_prompt = self._build_user_prompt(prompt, language)
        
        try:
            if self.provider == "openai":
                response = await self._call_openai(system_prompt, user_prompt, response_model, **kwargs)
            elif self.provider == "anthropic":
                response = await self._call_anthropic(system_prompt, user_prompt, **kwargs)
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
                
            return self._parse_response(response, language)
            
        except Exception as e:
            logger.error(f"Error generating code: {e}")
            raise
    
    async def _call_openai(
        self, 
        system_prompt: str, 
        user_prompt: str, 
        response_model: Optional[BaseModel] = None,
        **kwargs
    ) -> str:
        """Вызов OpenAI API"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        params = {
            "model": self.model,
            "messages": messages,
            "max_tokens": kwargs.get("max_tokens", 32768),
            "temperature": kwargs.get("temperature", 0.1),
        }
        
        # Добавляем structured output если передана модель
        if response_model:
            params["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": response_model.__name__,
                    "schema": response_model.model_json_schema()
                }
            }
        
        response = await self.client.chat.completions.create(**params)
        return response.choices[0].message.content
    
    async def _call_anthropic(
        self,
        system_prompt: str,
        user_prompt: str,
        **kwargs
    ) -> str:
        """Вызов Anthropic API"""
        
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=kwargs.get("max_tokens", 32768),
            temperature=kwargs.get("temperature", 0.1),
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        
        return response.content[0].text
    
    def _build_system_prompt(self, language: str) -> str:
        """Построение системного промпта с учетом языка программирования"""
        
        base_prompt = """
        <Role>
        Ты - экспертный программист с доступом к современным инструментам разработки через MCP.
        </Role>
        
        <Principles>
        1. Настойчивость: Продолжай работу до полного решения задачи
        2. Использование инструментов: Используй MCP-серверы для валидации и тестирования
        3. Планирование: Тщательно планируй каждый шаг перед выполнением
        </Principles>
        
        <Output_Format>
        Предоставляй ответ в следующем формате:
        
        **Код:**
        ```{language}
        # Твой код здесь
        ```
        
        **Зависимости:**
        - список зависимостей
        
        **Объяснение:**
        Краткое объяснение решения
        
        **Тесты:**
        ```{language}
        # Тесты для кода
        ```
        
        **Документация:**
        Краткая документация по использованию
        </Output_Format>
        """.format(language=language)
        
        # Добавляем специфичные для языка инструкции
        language_specifics = {
            "python": """
            <Python_Guidelines>
            - Используй type hints
            - Следуй PEP8
            - Добавляй docstrings
            - Используй современные возможности Python 3.12
            - Обрабатывай исключения
            </Python_Guidelines>
            """,
            
            "javascript": """
            <JavaScript_Guidelines>
            - Используй ES6+ синтаксис
            - Добавляй JSDoc комментарии
            - Следуй ESLint правилам
            - Используй async/await для асинхронного кода
            - Обрабатывай ошибки properly
            </JavaScript_Guidelines>
            """,
            
            "typescript": """
            <TypeScript_Guidelines>
            - Используй строгую типизацию
            - Определяй интерфейсы для сложных объектов
            - Используй generics где уместно
            - Добавляй TSDoc комментарии
            - Конфигурируй strict mode
            </TypeScript_Guidelines>
            """
        }
        
        return base_prompt + language_specifics.get(language, "")
    
    def _build_user_prompt(self, task: str, language: str) -> str:
        """Построение пользовательского промпта"""
        return f"""
        Задача: {task}
        
        Язык программирования: {language}
        
        Требования:
        1. Создай производственно-готовый код
        2. Включи обработку ошибок
        3. Добавь комментарии и документацию
        4. Создай тесты для проверки функциональности
        5. Укажи необходимые зависимости
        
        Используй доступные MCP-инструменты для:
        - Валидации синтаксиса
        - Проверки стиля кода
        - Поиска документации
        - Тестирования в sandbox
        """
    
    def _parse_response(self, response: str, language: str) -> CodeResponse:
        """Парсинг ответа LLM в структурированную модель"""
        
        # Простой парсер для извлечения секций из ответа
        lines = response.split('\n')
        
        code = ""
        dependencies = []
        explanation = ""
        tests = ""
        documentation = ""
        
        current_section = None
        current_content = []
        
        for line in lines:
            if "**Код:**" in line or "```" + language in line:
                if current_section:
                    self._process_section(current_section, current_content, 
                                        code, dependencies, explanation, tests, documentation)
                current_section = "code"
                current_content = []
            elif "**Зависимости:**" in line:
                if current_section:
                    self._process_section(current_section, current_content,
                                        code, dependencies, explanation, tests, documentation)
                current_section = "dependencies"
                current_content = []
            elif "**Объяснение:**" in line:
                if current_section:
                    self._process_section(current_section, current_content,
                                        code, dependencies, explanation, tests, documentation)
                current_section = "explanation"
                current_content = []
            elif "**Тесты:**" in line:
                if current_section:
                    self._process_section(current_section, current_content,
                                        code, dependencies, explanation, tests, documentation)
                current_section = "tests"
                current_content = []
            elif "**Документация:**" in line:
                if current_section:
                    self._process_section(current_section, current_content,
                                        code, dependencies, explanation, tests, documentation)
                current_section = "documentation"
                current_content = []
            else:
                if current_section and line.strip():
                    current_content.append(line)
        
        # Обрабатываем последнюю секцию
        if current_section:
            self._process_section(current_section, current_content,
                                code, dependencies, explanation, tests, documentation)
        
        return CodeResponse(
            code=code or response,  # Fallback to full response if parsing fails
            language=language,
            dependencies=dependencies,
            explanation=explanation,
            tests=tests,
            documentation=documentation
        )
    
    def _process_section(self, section: str, content: List[str], 
                        code: str, dependencies: List[str], explanation: str, 
                        tests: str, documentation: str):
        """Обработка секций ответа"""
        content_str = '\n'.join(content).strip()
        
        if section == "code":
            # Убираем маркеры кода блоков
            content_str = content_str.replace('```', '').strip()
            code = content_str
        elif section == "dependencies":
            # Извлекаем зависимости из списка
            for line in content:
                if line.strip().startswith('-'):
                    dependencies.append(line.strip()[1:].strip())
        elif section == "explanation":
            explanation = content_str
        elif section == "tests":
            content_str = content_str.replace('```', '').strip()
            tests = content_str
        elif section == "documentation":
            documentation = content_str
    
    async def validate_api_key(self) -> bool:
        """Валидация API ключа"""
        try:
            if self.provider == "openai":
                await self.client.models.list()
            elif self.provider == "anthropic":
                await self.client.messages.create(
                    model=self.model,
                    max_tokens=1,
                    messages=[{"role": "user", "content": "test"}]
                )
            return True
        except Exception as e:
            logger.error(f"API key validation failed: {e}")
            return False