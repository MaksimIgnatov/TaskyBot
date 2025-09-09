#!/bin/bash

# Скрипт для запуска TaskyBot с Docker Compose

set -e

echo "🤖 Запуск TaskyBot..."

# Проверяем наличие .env файла
if [ ! -f .env ]; then
    echo "❌ Файл .env не найден!"
    echo "📝 Скопируйте .env.example в .env и заполните BOT_TOKEN"
    echo "   cp .env.example .env"
    echo "   nano .env"
    exit 1
fi

# Проверяем наличие BOT_TOKEN в .env
if ! grep -q "BOT_TOKEN=" .env || grep -q "BOT_TOKEN=your_bot_token_here" .env; then
    echo "❌ BOT_TOKEN не установлен в .env файле!"
    echo "📝 Получите токен у @BotFather и добавьте в .env файл"
    exit 1
fi

# Создаем необходимые директории
mkdir -p data logs

# Запускаем с Docker Compose
echo "🐳 Запуск через Docker Compose..."
docker-compose up -d

echo "✅ TaskyBot запущен!"
echo "📊 Для просмотра логов: docker-compose logs -f"
echo "🛑 Для остановки: docker-compose down"
