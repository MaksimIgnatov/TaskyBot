"""
Модели данных для TaskyBot
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import os


class Task:
    """Класс для представления задачи"""
    
    def __init__(self, task_id: int, user_id: int, text: str, created_at: datetime = None):
        self.id = task_id
        self.user_id = user_id
        self.text = text
        self.completed = False
        self.created_at = created_at or datetime.now()
        self.reminder_minutes: Optional[int] = None
        self.reminder_set_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """Преобразование в словарь для сериализации"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'text': self.text,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'reminder_minutes': self.reminder_minutes,
            'reminder_set_at': self.reminder_set_at.isoformat() if self.reminder_set_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Создание объекта из словаря"""
        task = cls(
            task_id=data['id'],
            user_id=data['user_id'],
            text=data['text'],
            created_at=datetime.fromisoformat(data['created_at'])
        )
        task.completed = data['completed']
        task.reminder_minutes = data.get('reminder_minutes')
        task.reminder_set_at = datetime.fromisoformat(data['reminder_set_at']) if data.get('reminder_set_at') else None
        return task


class TaskManager:
    """Менеджер для управления задачами"""
    
    def __init__(self, data_file: str = "tasks.json"):
        self.data_file = data_file
        self.tasks: Dict[int, List[Task]] = {}  # user_id -> List[Task]
        self.next_task_id = 1
        self.load_tasks()
    
    def load_tasks(self) -> None:
        """Загрузка задач из файла"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = {}
                    for user_id_str, tasks_data in data.get('tasks', {}).items():
                        user_id = int(user_id_str)
                        self.tasks[user_id] = [Task.from_dict(task_data) for task_data in tasks_data]
                    self.next_task_id = data.get('next_task_id', 1)
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"Ошибка загрузки данных: {e}")
                self.tasks = {}
                self.next_task_id = 1
    
    def save_tasks(self) -> None:
        """Сохранение задач в файл"""
        try:
            data = {
                'tasks': {
                    str(user_id): [task.to_dict() for task in tasks]
                    for user_id, tasks in self.tasks.items()
                },
                'next_task_id': self.next_task_id
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения данных: {e}")
    
    def add_task(self, user_id: int, text: str) -> Task:
        """Добавление новой задачи"""
        if user_id not in self.tasks:
            self.tasks[user_id] = []
        
        task = Task(self.next_task_id, user_id, text)
        self.tasks[user_id].append(task)
        self.next_task_id += 1
        self.save_tasks()
        return task
    
    def get_user_tasks(self, user_id: int) -> List[Task]:
        """Получение всех задач пользователя"""
        return self.tasks.get(user_id, [])
    
    def get_task(self, user_id: int, task_id: int) -> Optional[Task]:
        """Получение конкретной задачи пользователя"""
        user_tasks = self.tasks.get(user_id, [])
        for task in user_tasks:
            if task.id == task_id:
                return task
        return None
    
    def mark_completed(self, user_id: int, task_id: int) -> bool:
        """Отметка задачи как выполненной"""
        task = self.get_task(user_id, task_id)
        if task and not task.completed:
            task.completed = True
            self.save_tasks()
            return True
        return False
    
    def delete_task(self, user_id: int, task_id: int) -> bool:
        """Удаление задачи"""
        user_tasks = self.tasks.get(user_id, [])
        for i, task in enumerate(user_tasks):
            if task.id == task_id:
                del user_tasks[i]
                self.save_tasks()
                return True
        return False
    
    def set_reminder(self, user_id: int, task_id: int, minutes: int) -> bool:
        """Установка напоминания для задачи"""
        task = self.get_task(user_id, task_id)
        if task and not task.completed:
            task.reminder_minutes = minutes
            task.reminder_set_at = datetime.now()
            self.save_tasks()
            return True
        return False
    
    def get_due_reminders(self, current_time: datetime) -> List[tuple]:
        """Получение задач, для которых пора отправить напоминание"""
        due_reminders = []
        
        for user_id, tasks in self.tasks.items():
            for task in tasks:
                if (task.reminder_minutes and 
                    task.reminder_set_at and 
                    not task.completed and
                    current_time >= task.reminder_set_at + timedelta(minutes=task.reminder_minutes)):
                    due_reminders.append((user_id, task))
        
        return due_reminders
    
    def clear_reminder(self, user_id: int, task_id: int) -> None:
        """Очистка напоминания после отправки"""
        task = self.get_task(user_id, task_id)
        if task:
            task.reminder_minutes = None
            task.reminder_set_at = None
            self.save_tasks()
