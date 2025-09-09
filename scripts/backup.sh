#!/bin/bash

# Скрипт для резервного копирования данных TaskyBot

set -e

BACKUP_DIR="backups"
DATE=$(date +%Y%m%d_%H%M%S)

echo "💾 Создание резервной копии данных TaskyBot..."

# Создаем директорию для бэкапов
mkdir -p "$BACKUP_DIR"

# Копируем файл данных
if [ -f "data/tasks.json" ]; then
    cp "data/tasks.json" "$BACKUP_DIR/tasks_$DATE.json"
    echo "✅ Резервная копия создана: $BACKUP_DIR/tasks_$DATE.json"
else
    echo "⚠️  Файл данных не найден: data/tasks.json"
fi

# Удаляем старые бэкапы (старше 7 дней)
find "$BACKUP_DIR" -name "tasks_*.json" -mtime +7 -delete 2>/dev/null || true

echo "🧹 Старые резервные копии (старше 7 дней) удалены"
echo "📁 Все резервные копии: ls -la $BACKUP_DIR/"
