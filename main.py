#!/usr/bin/env python3
"""
TaskyBot - Telegram бот для управления задачами с напоминаниями
"""

import asyncio
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import TelegramError

from models import Task, TaskManager
from config import BOT_TOKEN

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Глобальный менеджер задач
task_manager = TaskManager()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    welcome_message = """
🤖 Добро пожаловать в TaskyBot!

Доступные команды:
/add <текст> — добавить задачу
/list — вывести список задач
/done <id> — отметить задачу выполненной
/delete <id> — удалить задачу
/remind <id> <минуты> — установить напоминание

Начните с добавления своей первой задачи!
    """
    await update.message.reply_text(welcome_message)


async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /add"""
    if not context.args:
        await update.message.reply_text("❌ Пожалуйста, укажите текст задачи.\nИспользование: /add <текст задачи>")
        return
    
    user_id = update.effective_user.id
    task_text = " ".join(context.args)
    
    task = task_manager.add_task(user_id, task_text)
    await update.message.reply_text(f"✅ Задача добавлена!\nID: {task.id}\nТекст: {task.text}")


async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /list"""
    user_id = update.effective_user.id
    tasks = task_manager.get_user_tasks(user_id)
    
    if not tasks:
        await update.message.reply_text("📝 У вас пока нет задач. Добавьте первую с помощью /add")
        return
    
    message = "📋 Ваши задачи:\n\n"
    for task in tasks:
        status = "✅" if task.completed else "⏳"
        reminder_text = f" (напоминание через {task.reminder_minutes} мин)" if task.reminder_minutes else ""
        message += f"{status} ID: {task.id} | {task.text}{reminder_text}\n"
    
    await update.message.reply_text(message)


async def done_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /done"""
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("❌ Пожалуйста, укажите корректный ID задачи.\nИспользование: /done <id>")
        return
    
    user_id = update.effective_user.id
    task_id = int(context.args[0])
    
    if task_manager.mark_completed(user_id, task_id):
        await update.message.reply_text(f"✅ Задача {task_id} отмечена как выполненная!")
    else:
        await update.message.reply_text(f"❌ Задача с ID {task_id} не найдена или уже выполнена.")


async def delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /delete"""
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("❌ Пожалуйста, укажите корректный ID задачи.\nИспользование: /delete <id>")
        return
    
    user_id = update.effective_user.id
    task_id = int(context.args[0])
    
    if task_manager.delete_task(user_id, task_id):
        await update.message.reply_text(f"🗑️ Задача {task_id} удалена!")
    else:
        await update.message.reply_text(f"❌ Задача с ID {task_id} не найдена.")


async def set_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /remind"""
    if len(context.args) != 2 or not context.args[0].isdigit() or not context.args[1].isdigit():
        await update.message.reply_text("❌ Пожалуйста, укажите корректные параметры.\nИспользование: /remind <id> <минуты>")
        return
    
    user_id = update.effective_user.id
    task_id = int(context.args[0])
    minutes = int(context.args[1])
    
    if minutes <= 0:
        await update.message.reply_text("❌ Время напоминания должно быть больше 0 минут.")
        return
    
    if task_manager.set_reminder(user_id, task_id, minutes):
        await update.message.reply_text(f"⏰ Напоминание установлено! Задача {task_id} будет напомнена через {minutes} минут.")
    else:
        await update.message.reply_text(f"❌ Задача с ID {task_id} не найдена.")


async def check_reminders(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Проверка напоминаний каждые 30 секунд"""
    try:
        current_time = datetime.now()
        reminders_to_send = task_manager.get_due_reminders(current_time)
        
        for user_id, task in reminders_to_send:
            try:
                message = f"⏰ Напоминание!\n\nЗадача: {task.text}\nВремя создания: {task.created_at.strftime('%d.%m.%Y %H:%M')}"
                await context.bot.send_message(chat_id=user_id, text=message)
                
                # Удаляем напоминание после отправки
                task_manager.clear_reminder(task.user_id, task.id)
                logger.info(f"Отправлено напоминание пользователю {user_id} для задачи {task.id}")
                
            except TelegramError as e:
                logger.error(f"Ошибка отправки напоминания пользователю {user_id}: {e}")
                
    except Exception as e:
        logger.error(f"Ошибка при проверке напоминаний: {e}")


def main() -> None:
    """Основная функция запуска бота"""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add_task))
    application.add_handler(CommandHandler("list", list_tasks))
    application.add_handler(CommandHandler("done", done_task))
    application.add_handler(CommandHandler("delete", delete_task))
    application.add_handler(CommandHandler("remind", set_reminder))
    
    # Настраиваем периодическую проверку напоминаний
    job_queue = application.job_queue
    job_queue.run_repeating(check_reminders, interval=30, first=10)
    
    # Запускаем бота
    logger.info("Запуск TaskyBot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
