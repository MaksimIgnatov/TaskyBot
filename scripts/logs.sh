#!/bin/bash

# Скрипт для просмотра логов TaskyBot

echo "📊 Просмотр логов TaskyBot..."
echo "💡 Для выхода нажмите Ctrl+C"
echo ""

# Показываем логи в реальном времени
docker-compose logs -f taskybot
