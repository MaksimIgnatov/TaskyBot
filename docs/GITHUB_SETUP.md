# Настройка GitHub репозитория

## Создание репозитория на GitHub

1. Перейдите на [GitHub.com](https://github.com) и войдите в свой аккаунт
2. Нажмите кнопку "New repository" или перейдите по ссылке [github.com/new](https://github.com/new)
3. Заполните форму:
   - **Repository name**: `tg-bot` или `taskybot`
   - **Description**: `TaskyBot - Telegram bot for task management with reminders`
   - **Visibility**: Public (или Private, если хотите)
   - **Initialize repository**: НЕ ставьте галочки (у нас уже есть код)
4. Нажмите "Create repository"

## Подключение локального репозитория к GitHub

После создания репозитория на GitHub выполните следующие команды:

```bash
# Добавьте удаленный репозиторий (замените YOUR_USERNAME на ваш GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/tg-bot.git

# Переименуйте ветку в main (если нужно)
git branch -M main

# Отправьте код в GitHub
git push -u origin main
```

## Альтернативный способ через GitHub CLI

Если у вас установлен GitHub CLI:

```bash
# Создайте репозиторий и отправьте код одной командой
gh repo create tg-bot --public --description "TaskyBot - Telegram bot for task management with reminders" --source=. --remote=origin --push
```

## Проверка

После успешной отправки:
1. Перейдите на страницу вашего репозитория на GitHub
2. Убедитесь, что все файлы загружены
3. Проверьте, что README.md отображается корректно

## Дальнейшая работа

Для отправки изменений в будущем:

```bash
# Добавьте изменения
git add .

# Сделайте коммит
git commit -m "Описание изменений"

# Отправьте в GitHub
git push
```

## Настройка GitHub Actions (опционально)

Для автоматического тестирования и развертывания можно добавить GitHub Actions:

1. Создайте файл `.github/workflows/ci.yml`
2. Настройте автоматические тесты при каждом push
3. Настройте автоматическое развертывание на сервер

Пример базового CI файла:

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Lint with flake8
      run: |
        pip install flake8
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

## Полезные ссылки

- [GitHub Docs](https://docs.github.com/)
- [GitHub CLI](https://cli.github.com/)
- [GitHub Actions](https://github.com/features/actions)
