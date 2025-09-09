# Руководство по развертыванию TaskyBot

## Локальное развертывание

### 1. Подготовка окружения

```bash
# Создайте виртуальное окружение
python -m venv venv

# Активируйте виртуальное окружение
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt
```

### 2. Настройка бота

1. Откройте Telegram и найдите [@BotFather](https://t.me/BotFather)
2. Отправьте команду `/newbot`
3. Введите имя бота (например: "My TaskyBot")
4. Введите username бота (например: "my_tasky_bot")
5. Скопируйте полученный токен

### 3. Настройка переменных окружения

```bash
# Windows
set BOT_TOKEN=your_bot_token_here

# Linux/Mac
export BOT_TOKEN=your_bot_token_here
```

### 4. Запуск бота

```bash
python main.py
```

## Развертывание на сервере

### Использование systemd (Linux)

1. Создайте файл сервиса `/etc/systemd/system/taskybot.service`:

```ini
[Unit]
Description=TaskyBot Telegram Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/tg-bot
Environment=BOT_TOKEN=your_bot_token_here
ExecStart=/path/to/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

2. Включите и запустите сервис:

```bash
sudo systemctl enable taskybot
sudo systemctl start taskybot
sudo systemctl status taskybot
```

### Использование Docker

1. Создайте `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

2. Создайте `docker-compose.yml`:

```yaml
version: '3.8'

services:
  taskybot:
    build: .
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
    volumes:
      - ./tasks.json:/app/tasks.json
    restart: unless-stopped
```

3. Запустите контейнер:

```bash
# Создайте .env файл с токеном
echo "BOT_TOKEN=your_bot_token_here" > .env

# Запустите
docker-compose up -d
```

### Использование Heroku

1. Создайте `Procfile`:

```
worker: python main.py
```

2. Установите переменные окружения в Heroku:

```bash
heroku config:set BOT_TOKEN=your_bot_token_here
```

3. Разверните приложение:

```bash
git add .
git commit -m "Deploy TaskyBot"
git push heroku main
```

## Мониторинг и логирование

### Логирование

Бот автоматически логирует:
- Запуск и остановку
- Ошибки отправки сообщений
- Ошибки при проверке напоминаний

Логи выводятся в консоль в формате:
```
2024-01-01 12:00:00,000 - main - INFO - Запуск TaskyBot...
```

### Мониторинг

Для мониторинга работы бота можно использовать:

1. **systemd status** (если используете systemd):
```bash
sudo systemctl status taskybot
```

2. **Docker logs** (если используете Docker):
```bash
docker-compose logs -f taskybot
```

3. **Heroku logs** (если используете Heroku):
```bash
heroku logs --tail
```

## Резервное копирование

### Автоматическое резервное копирование

Создайте скрипт `backup.sh`:

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp tasks.json "backup/tasks_$DATE.json"
find backup/ -name "tasks_*.json" -mtime +7 -delete
```

Добавьте в crontab для ежедневного резервного копирования:

```bash
0 2 * * * /path/to/backup.sh
```

## Обновление бота

1. Остановите бота
2. Сделайте резервную копию `tasks.json`
3. Обновите код
4. Установите новые зависимости (если есть)
5. Запустите бота

## Безопасность

### Рекомендации

1. **Никогда не коммитьте токен бота** в репозиторий
2. Используйте переменные окружения для конфиденциальных данных
3. Регулярно обновляйте зависимости
4. Используйте HTTPS для веб-хуков (если планируете)
5. Ограничьте доступ к серверу с ботом

### Проверка безопасности

```bash
# Проверьте, что токен не в коде
grep -r "BOT_TOKEN" . --exclude-dir=.git

# Проверьте права доступа к файлам
ls -la tasks.json
```

## Устранение неполадок

### Частые проблемы

1. **Бот не отвечает**:
   - Проверьте правильность токена
   - Убедитесь, что бот запущен
   - Проверьте логи на ошибки

2. **Ошибки отправки сообщений**:
   - Пользователь заблокировал бота
   - Проблемы с сетью
   - Неверный chat_id

3. **Напоминания не работают**:
   - Проверьте, что бот работает постоянно
   - Убедитесь в правильности времени системы
   - Проверьте логи на ошибки

### Полезные команды

```bash
# Проверка статуса бота
ps aux | grep python

# Проверка логов
tail -f /var/log/syslog | grep taskybot

# Проверка файла данных
cat tasks.json | jq .
```
