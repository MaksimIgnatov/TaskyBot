#!/bin/bash

# Скрипт для остановки TaskyBot

set -e

echo "🛑 Остановка TaskyBot..."

# Останавливаем контейнеры
docker-compose down

echo "✅ TaskyBot остановлен!"
echo "📁 Данные сохранены в директории ./data/"
