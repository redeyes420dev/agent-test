# 🤖 Агент автоматизированной разработки кода

Мульти-агентная система для генерации, тестирования и валидации кода с интеграцией Model Context Protocol (MCP) и поддержкой GPT-4.1-mini.

## 🚀 Особенности

- **Мульти-агентная архитектура** на основе LangGraph с тремя специализированными агентами
- **Интеграция GPT-4.1-mini** - самая современная модель для кодирования
- **Model Context Protocol (MCP)** для расширяемости и интеграции с внешними сервисами
- **Веб-интерфейс** на React для удобного управления
- **Безопасное управление API ключами** с шифрованием
- **Git интеграция** для работы с репозиториями
- **Поддержка множественных языков программирования**
- **Автоматическое тестирование** и валидация кода
- **Мониторинг и аналитика** использования

## 🏗️ Архитектура

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Агент-        │    │  Агент-         │    │  Агент-         │
│  программист   │───▶│  тестировщик    │───▶│  валидатор      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ MCP Sandbox     │    │ MCP Testing     │    │ MCP Quality     │
│ Server          │    │ Server          │    │ Server          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Агенты системы

1. **Агент-программист**: Генерирует код на основе требований пользователя
2. **Агент-тестировщик**: Создает unit-тесты и интеграционные тесты
3. **Агент-валидатор**: Проверяет качество кода и соответствие стандартам

### MCP серверы

- **Sandbox Server**: Безопасное выполнение кода
- **Testing Server**: Автоматическое тестирование
- **Documentation Server**: Доступ к актуальной документации
- **GitHub Server**: Интеграция с Git репозиториями
- **Bright Data Server**: Веб-исследования и данные

## 📋 Требования

- Python 3.12+
- Node.js 18+
- Docker и Docker Compose
- PostgreSQL 15+
- Redis 7+

## ⚡ Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-org/coding-agent.git
cd coding-agent
```

### 2. Настройка переменных окружения

```bash
cp .env.example .env
```

Отредактируйте `.env` файл и добавьте ваши API ключи:

```env
# Обязательные ключи
OPENAI_API_KEY=sk-your-openai-api-key-here
GITHUB_TOKEN=ghp_your-github-token-here
ENCRYPTION_KEY=your-encryption-key-here

# Опциональные ключи
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
BRIGHTDATA_TOKEN=your-brightdata-token-here
```

### 3. Запуск с Docker Compose

```bash
# Запуск всех сервисов
docker-compose up -d

# Проверка статуса
docker-compose ps

# Просмотр логов
docker-compose logs -f coding-agent
```

### 4. Локальная разработка

```bash
# Установка зависимостей Python
pip install -r requirements.txt

# Установка MCP серверов
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-docs
npm install -g @brightdata/mcp

# Запуск базы данных
docker-compose up -d postgres redis

# Запуск приложения
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Настройка frontend

```bash
cd frontend
npm install
npm start
```

## 🔧 Конфигурация API ключей

### Через веб-интерфейс

1. Откройте http://localhost:3000
2. Перейдите в раздел "Настройки API"
3. Добавьте ваши API ключи для различных провайдеров

### Поддерживаемые провайдеры

| Провайдер | Модель | Назначение |
|-----------|--------|------------|
| OpenAI | GPT-4.1-mini | Основная генерация кода |
| Anthropic | Claude-3.5-Sonnet | Альтернативная модель |
| GitHub | - | Git операции и поиск кода |
| Bright Data | - | Веб-исследования |
| Google | Gemini Pro | Дополнительная модель |

## 🛠️ Использование

### Генерация кода через API

```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "task": "Создай REST API для управления пользователями",
    "language": "python",
    "framework": "FastAPI"
  }'
```

### Работа с Git репозиториями

```bash
# Клонирование репозитория
curl -X POST http://localhost:8000/api/repos/clone \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://github.com/user/repo.git",
    "token": "ghp_your_token",
    "branch": "main"
  }'
```

### WebSocket для real-time обновлений

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = function(event) {
  const data = JSON.parse(event.data);
  console.log('Статус:', data.status);
  console.log('Сообщение:', data.message);
};
```

## 🧪 Примеры использования

### Пример 1: Создание веб-приложения

```python
from coding_agent.main import CodingAgentSystem

async def create_web_app():
    agent = CodingAgentSystem()
    
    result = await agent.generate_code(
        task="Создай веб-приложение для управления задачами с возможностью добавления, редактирования и удаления задач",
        language="python",
        framework="FastAPI",
        include_tests=True,
        include_frontend=True
    )
    
    print(f"Код: {result.code}")
    print(f"Тесты: {result.tests}")
    print(f"Frontend: {result.frontend_code}")
```

### Пример 2: Анализ существующего кода

```python
result = await agent.analyze_code(
    repo_path="./my-project",
    language="python",
    checks=["security", "performance", "style"]
)

print(f"Проблемы безопасности: {result.security_issues}")
print(f"Рекомендации: {result.recommendations}")
```

### Пример 3: Автоматическое тестирование

```python
test_result = await agent.run_tests(
    code=my_code,
    language="python",
    test_types=["unit", "integration", "performance"]
)

print(f"Покрытие: {test_result.coverage}%")
print(f"Результаты: {test_result.results}")
```

## 🔒 Безопасность

### Шифрование API ключей

Все API ключи шифруются с использованием `cryptography.fernet` перед сохранением:

```python
# Генерация ключа шифрования
from cryptography.fernet import Fernet
encryption_key = Fernet.generate_key()
```

### Изоляция выполнения кода

Код выполняется в изолированных Docker контейнерах с ограничениями:

- Ограничение памяти: 512MB
- Ограничение CPU: 1 ядро
- Ограничение времени: 30 секунд
- Отсутствие сетевого доступа

### Аутентификация и авторизация

- JWT токены для API доступа
- Роли пользователей (admin, developer, viewer)
- Rate limiting: 60 запросов в минуту

## 📊 Мониторинг

### Метрики Prometheus

- Количество запросов к агентам
- Время отклика MCP серверов
- Использование API ключей
- Ошибки и исключения

### Grafana Dashboard

Доступен по адресу: http://localhost:3001
- Логин: admin
- Пароль: admin

### Основные метрики:

- **Производительность агентов**
- **Статистика использования API**
- **Мониторинг MCP серверов**
- **Анализ ошибок**

## 🧩 Расширение функциональности

### Добавление нового MCP сервера

1. Создайте конфигурацию сервера:

```python
# config/mcp_servers.py
new_server = {
    "name": "my_custom_server",
    "command": "python",
    "args": ["-m", "my_mcp_server"],
    "env": {"API_KEY": "your-key"}
}
```

2. Добавьте в список серверов в настройках

3. Перезапустите приложение

### Создание пользовательского агента

```python
from coding_agent.agents.base import BaseAgent

class CustomAgent(BaseAgent):
    async def process(self, task: str, context: dict) -> dict:
        # Ваша логика обработки
        return {"result": "custom result"}
```

### Интеграция с новыми LLM провайдерами

```python
from coding_agent.core.llm_client import LLMClient

class CustomLLMClient(LLMClient):
    def __init__(self, api_key: str):
        self.api_key = api_key
        # Инициализация вашего клиента
```

## 🚨 Устранение неполадок

### Общие проблемы

**Ошибка: "MCP server connection failed"**
```bash
# Проверка статуса MCP серверов
docker-compose ps mcp-*

# Перезапуск MCP серверов
docker-compose restart mcp-sandbox mcp-testing
```

**Ошибка: "API key validation failed"**
- Проверьте правильность API ключа
- Убедитесь, что у ключа есть необходимые права
- Проверьте лимиты использования

**Ошибка: "Database connection failed"**
```bash
# Проверка PostgreSQL
docker-compose logs postgres

# Пересоздание базы данных
docker-compose down -v
docker-compose up -d postgres
```

### Логирование

```bash
# Просмотр логов приложения
docker-compose logs -f coding-agent

# Логи MCP серверов
docker-compose logs -f mcp-sandbox

# Логи базы данных
docker-compose logs -f postgres
```

### Отладка

Включите режим отладки в `.env`:

```env
DEBUG_MODE=true
LOG_LEVEL=DEBUG
SQL_ECHO=true
```

## 📈 Производительность

### Рекомендации по оптимизации

1. **Используйте Redis кэширование** для частых запросов
2. **Настройте пул соединений** к базе данных
3. **Ограничьте количество воркеров** в зависимости от ресурсов
4. **Мониторьте использование памяти** MCP серверов

### Масштабирование

```yaml
# docker-compose.override.yml
version: '3.8'
services:
  coding-agent:
    deploy:
      replicas: 3
    environment:
      - WORKERS=2
```

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для функциональности (`git checkout -b feature/AmazingFeature`)
3. Зафиксируйте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Отправьте в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

### Стандарты кода

- Используйте `black` для форматирования Python кода
- Покрытие тестами должно быть не менее 80%
- Добавляйте docstrings для всех публичных функций
- Следуйте принципам SOLID

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 📞 Поддержка

- **Issues**: [GitHub Issues](https://github.com/your-org/coding-agent/issues)
- **Документация**: [Wiki](https://github.com/your-org/coding-agent/wiki)
- **Email**: support@your-domain.com

## 🙏 Благодарности

- [OpenAI](https://openai.com/) за GPT-4.1-mini
- [Anthropic](https://anthropic.com/) за Model Context Protocol
- [LangChain](https://langchain.com/) за LangGraph
- Сообщество разработчиков за вклад и обратную связь

---

**Сделано с ❤️ командой разработчиков**