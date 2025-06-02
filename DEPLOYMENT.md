# 🎯 Инструкции по развертыванию агента разработки

## 📋 Что создано

В результате работы был создан полнофункциональный проект агента автоматизированной разработки кода:

### Ключевые компоненты:
1. **Backend на FastAPI** с интеграцией GPT-4.1-mini
2. **Model Context Protocol (MCP)** для расширяемости  
3. **Веб-интерфейс на React** для управления системой
4. **Безопасная система API ключей** с шифрованием
5. **Git интеграция** для работы с репозиториями
6. **Docker конфигурация** для легкого развертывания

## 🚀 Развертывание

### Способ 1: Быстрый запуск (Рекомендуется)

```bash
# 1. Сделайте скрипт исполняемым
chmod +x start.sh

# 2. Запустите автоматическую установку
./start.sh

# 3. Следуйте инструкциям скрипта
```

### Способ 2: Ручная настройка

```bash
# 1. Клонирование и настройка
git clone <your-repo>
cd coding-agent

# 2. Настройка окружения
cp .env.example .env
# Отредактируйте .env и добавьте API ключи

# 3. Запуск через Docker
docker-compose up -d

# 4. Проверка статуса
curl http://localhost:8000/health
```

## 🔑 Обязательные API ключи

Для работы системы необходимо настроить следующие ключи в `.env`:

```env
# ОБЯЗАТЕЛЬНО - OpenAI для GPT-4.1-mini
OPENAI_API_KEY=sk-your-openai-key-here

# РЕКОМЕНДУЕТСЯ - GitHub для MCP интеграции  
GITHUB_TOKEN=ghp_your-github-token-here

# ОПЦИОНАЛЬНО - дополнительные провайдеры
ANTHROPIC_API_KEY=sk-ant-your-key-here
BRIGHTDATA_TOKEN=your-brightdata-token-here
```

## 🌐 Доступ к приложению

После успешного запуска будут доступны:

- **Основное приложение**: http://localhost:8000
- **API документация**: http://localhost:8000/docs  
- **Веб-демо**: [Демо интерфейс](https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/ba3e941a4a5ae65ea58ab8cd50761c98/4d1ff75e-e8e3-4b09-b759-3739673c09b9/index.html)
- **Мониторинг Grafana**: http://localhost:3001
- **Метрики Prometheus**: http://localhost:9090

## 🔧 Первоначальная настройка

### 1. Добавление API ключей через веб-интерфейс

1. Откройте демо интерфейс или http://localhost:3000
2. Перейдите в раздел "API Ключи"
3. Добавьте ваши ключи для разных провайдеров
4. Система автоматически проверит их валидность

### 2. Тестирование генерации кода

```bash
# Тест через API
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Создай простой калькулятор на Python",
    "language": "python"
  }'
```

### 3. Работа с Git репозиториями  

```bash
# Клонирование репозитория
curl -X POST http://localhost:8000/api/repos/clone \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://github.com/user/repo.git",
    "token": "YOUR_GITHUB_TOKEN"
  }'
```

## 🛠️ Архитектура MCP

Система использует Model Context Protocol для интеграции с внешними сервисами:

### Подключенные MCP серверы:
- **Sandbox Server**: Безопасное выполнение кода
- **Testing Server**: Автоматическое тестирование  
- **Documentation Server**: Доступ к документации
- **GitHub Server**: Git операции
- **Bright Data Server**: Веб-исследования

### Проверка статуса MCP:
```bash
curl http://localhost:8000/api/status
```

## 📊 Мониторинг и логи

### Просмотр логов:
```bash
# Логи основного приложения
docker-compose logs -f coding-agent

# Логи MCP серверов
docker-compose logs -f mcp-sandbox mcp-testing

# Логи базы данных
docker-compose logs -f postgres
```

### Метрики в Grafana:
- Производительность агентов
- Использование API ключей  
- Статистика MCP серверов
- Ошибки и исключения

## 🔒 Безопасность

### Встроенные механизмы:
- **Шифрование API ключей** с использованием Fernet
- **Изоляция выполнения кода** в Docker контейнерах
- **JWT аутентификация** для API доступа
- **Rate limiting**: 60 запросов в минуту
- **Валидация входных данных** на всех уровнях

### Настройка безопасности:
```env
# Сгенерируйте новые ключи для продакшена
ENCRYPTION_KEY=<новый-ключ-fernet>
JWT_SECRET=<случайная-строка-32-символа>
```

## 📁 Структура проекта

```
coding-agent/
├── main.py                 # Точка входа FastAPI
├── requirements.txt        # Python зависимости
├── docker-compose.yml      # Docker конфигурация
├── .env.example           # Пример переменных окружения
├── start.sh               # Скрипт автозапуска
├── coding_agent/          # Основной код
│   ├── core/             # Ядро системы (LLM, MCP)
│   ├── agents/           # Агенты (программист, тестировщик, валидатор)
│   ├── api/              # REST API эндпоинты
│   ├── security/         # Шифрование и аутентификация
│   └── tools/            # Инструменты (Git, выполнение кода)
└── frontend/             # React приложение
```

## 🧪 Примеры использования

### Генерация веб-API:
```python
# Через Python SDK
from coding_agent.main import CodingAgentSystem

agent = CodingAgentSystem()
result = await agent.generate_code(
    task="Создай REST API для блога",
    language="python",
    framework="FastAPI"
)
```

### Анализ существующего кода:
```python
result = await agent.analyze_code(
    repo_path="./my-project",
    checks=["security", "performance", "style"]
)
```

## 🚨 Устранение неполадок

### Частые проблемы:

**"MCP server connection failed"**
```bash
docker-compose restart mcp-sandbox mcp-testing
```

**"API key validation failed"**  
- Проверьте правильность ключа в .env
- Убедитесь в наличии прав доступа

**"Database connection failed"**
```bash
docker-compose down -v
docker-compose up -d postgres
```

### Включение отладки:
```env
DEBUG_MODE=true
LOG_LEVEL=DEBUG
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи: `docker-compose logs -f`
2. Убедитесь в наличии всех API ключей
3. Проверьте статус сервисов: `docker-compose ps`
4. Обратитесь к документации в README.md

## 🎉 Готово!

Ваш агент автоматизированной разработки кода готов к использованию! 

**Возможности:**
- ✅ Генерация кода на Python, JavaScript, TypeScript, Java
- ✅ Автоматическое тестирование и валидация
- ✅ Интеграция с GitHub репозиториями  
- ✅ Безопасное управление API ключами
- ✅ Real-time мониторинг и аналитика
- ✅ Расширяемость через MCP серверы

**Начните с простой задачи в веб-интерфейсе и получите готовый код с тестами!** 🚀