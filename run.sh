#!/bin/bash
# run.sh - Запуск системы Coding Agent

echo "🚀 Запуск системы Coding Agent..."

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python 3.10+"
    exit 1
fi

# Проверяем виртуальное окружение
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Рекомендуется использовать виртуальное окружение"
    echo "   Создайте его командой: python3 -m venv .venv && source .venv/bin/activate"
fi

# Устанавливаем зависимости если нужно
if [ ! -f ".deps_installed" ]; then
    echo "📦 Устанавливаем зависимости..."
    pip install -r requirements.txt
    touch .deps_installed
fi

# Запускаем систему
echo "🌟 Запуск основного приложения..."
python main.py