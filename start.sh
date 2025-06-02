#!/bin/bash

# Скрипт быстрого запуска агента разработки
# Этот скрипт автоматически настроит и запустит всю систему

set -e

echo "🚀 Запуск агента автоматизированной разработки кода"
echo "=================================================="

# Проверка зависимостей
check_dependency() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 не установлен. Установите его и попробуйте снова."
        exit 1
    else
        echo "✅ $1 найден"
    fi
}

echo "🔍 Проверка зависимостей..."
check_dependency "docker"
check_dependency "docker-compose"
check_dependency "python3"
check_dependency "node"

# Проверка версии Python
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [[ "$PYTHON_VERSION" < "3.12" ]]; then
    echo "❌ Требуется Python 3.12+, найден $PYTHON_VERSION"
    exit 1
else
    echo "✅ Python $PYTHON_VERSION"
fi

# Создание .env файла если его нет
if [ ! -f .env ]; then
    echo "📄 Создание .env файла..."
    cp .env.example .env
    
    # Генерация ключа шифрования
    ENCRYPTION_KEY=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
    sed -i "s/your-encryption-key-here/$ENCRYPTION_KEY/" .env
    
    # Генерация JWT секрета
    JWT_SECRET=$(openssl rand -base64 32)
    sed -i "s/your-super-secret-jwt-key-here/$JWT_SECRET/" .env
    
    echo "🔐 Сгенерированы ключи безопасности"
    echo ""
    echo "⚠️  ВАЖНО: Отредактируйте .env файл и добавьте ваши API ключи:"
    echo "   - OPENAI_API_KEY (обязательно)"
    echo "   - GITHUB_TOKEN (рекомендуется)"
    echo "   - ANTHROPIC_API_KEY (опционально)"
    echo "   - BRIGHTDATA_TOKEN (опционально)"
    echo ""
    read -p "Нажмите Enter после настройки API ключей..."
fi

# Проверка наличия обязательных ключей
if ! grep -q "sk-" .env && ! grep -q "your-openai-api-key-here" .env; then
    echo "❌ OpenAI API ключ не настроен в .env файле"
    echo "Получите ключ на: https://platform.openai.com/api-keys"
    exit 1
fi

# Создание необходимых директорий
echo "📁 Создание директорий..."
mkdir -p repos logs data/postgres data/redis

# Установка Python зависимостей
echo "📦 Установка Python зависимостей..."
if [ -f requirements.txt ]; then
    pip3 install -r requirements.txt
else
    echo "❌ Файл requirements.txt не найден"
    exit 1
fi

# Установка Node.js зависимостей для MCP серверов
echo "📦 Установка MCP серверов..."
npm install -g @modelcontextprotocol/server-github || echo "⚠️  Не удалось установить GitHub MCP сервер"
npm install -g @modelcontextprotocol/server-docs || echo "⚠️  Не удалось установить Documentation MCP сервер"
npm install -g @brightdata/mcp || echo "⚠️  Не удалось установить Bright Data MCP сервер"

# Запуск Docker Compose
echo "🐋 Запуск Docker контейнеров..."
docker-compose down -v 2>/dev/null || true  # Очистка предыдущих контейнеров
docker-compose up -d

# Ожидание запуска сервисов
echo "⏳ Ожидание запуска сервисов..."
sleep 10

# Проверка здоровья сервисов
check_service() {
    local service_name=$1
    local url=$2
    local max_attempts=30
    local attempt=1
    
    echo "🔍 Проверка $service_name..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s $url > /dev/null 2>&1; then
            echo "✅ $service_name работает"
            return 0
        fi
        
        echo "⏳ Попытка $attempt/$max_attempts..."
        sleep 2
        ((attempt++))
    done
    
    echo "❌ $service_name не отвечает"
    return 1
}

# Проверка основных сервисов
check_service "Основное приложение" "http://localhost:8000/health"
check_service "База данных PostgreSQL" "http://localhost:5432" || true
check_service "Redis" "http://localhost:6379" || true

# Проверка статуса через API
echo "🔍 Проверка статуса агентов..."
if curl -s http://localhost:8000/api/status | grep -q "agents_available"; then
    echo "✅ Агенты готовы к работе"
else
    echo "⚠️  Агенты еще инициализируются..."
fi

# Создание первого пользователя (опционально)
if [ "$1" = "--create-user" ]; then
    echo "👤 Создание тестового пользователя..."
    python3 -c "
import asyncio
from coding_agent.auth import create_user

async def main():
    user = await create_user('admin', 'admin@example.com', 'admin123')
    print(f'Создан пользователь: {user.username}')

asyncio.run(main())
    "
fi

# Вывод информации о запуске
echo ""
echo "🎉 Агент автоматизированной разработки успешно запущен!"
echo "=================================================="
echo ""
echo "📊 Доступные сервисы:"
echo "   • Основное приложение: http://localhost:8000"
echo "   • API документация:    http://localhost:8000/docs"
echo "   • Frontend (если запущен): http://localhost:3000"
echo "   • Grafana мониторинг:  http://localhost:3001 (admin/admin)"
echo "   • Prometheus метрики:  http://localhost:9090"
echo ""
echo "🔧 Управление:"
echo "   • Остановка:     docker-compose down"
echo "   • Перезапуск:    docker-compose restart"
echo "   • Логи:          docker-compose logs -f"
echo "   • Статус:        docker-compose ps"
echo ""
echo "📖 Документация: README.md"
echo ""

# Тестовый запрос к API
echo "🧪 Тестирование API..."
if response=$(curl -s http://localhost:8000/health); then
    echo "✅ API отвечает: $response"
else
    echo "❌ API не отвечает"
fi

echo ""
echo "🚀 Система готова к использованию!"

# Опциональный запуск frontend
read -p "Запустить React frontend? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -d "frontend" ]; then
        echo "🎨 Запуск React frontend..."
        cd frontend
        npm install
        npm start &
        cd ..
        echo "✅ Frontend запущен на http://localhost:3000"
    else
        echo "❌ Директория frontend не найдена"
    fi
fi

echo ""
echo "💡 Полезные команды:"
echo "   • Добавить API ключ: curl -X POST http://localhost:8000/api/keys -d '{...}'"
echo "   • Генерация кода:    curl -X POST http://localhost:8000/api/generate -d '{...}'"
echo "   • WebSocket:         ws://localhost:8000/ws"
echo ""
echo "Наслаждайтесь использованием агента! 🎯"