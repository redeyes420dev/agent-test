# Docker конфигурация для агента разработки
FROM python:3.12-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование файлов зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Установка Node.js зависимостей для MCP серверов
RUN npm install -g @modelcontextprotocol/server-github \
    @modelcontextprotocol/server-docs \
    @brightdata/mcp

# Копирование исходного кода
COPY . .

# Создание директорий для Git workspace и логов
RUN mkdir -p /app/repos /app/logs

# Установка переменных окружения
ENV PYTHONPATH=/app
ENV GIT_WORKSPACE=/app/repos
ENV LOG_LEVEL=INFO

# Создание пользователя для безопасности
RUN useradd -m -u 1000 coding_agent && \
    chown -R coding_agent:coding_agent /app
USER coding_agent

# Открытие порта
EXPOSE 8000

# Команда запуска
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]