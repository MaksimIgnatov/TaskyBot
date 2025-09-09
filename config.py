"""
Конфигурация для TaskyBot
"""

import os
from typing import Optional

# Токен бота - должен быть установлен в переменной окружения
BOT_TOKEN: Optional[str] = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError(
        "Необходимо установить переменную окружения BOT_TOKEN. "
        "Получите токен у @BotFather в Telegram и установите его:\n"
        "Windows: set BOT_TOKEN=your_token_here\n"
        "Linux/Mac: export BOT_TOKEN=your_token_here"
    )

# Настройки базы данных
DATA_FILE = "tasks.json"

# Настройки напоминаний
REMINDER_CHECK_INTERVAL = 30  # секунды

# Настройки логирования
LOG_LEVEL = "INFO"
