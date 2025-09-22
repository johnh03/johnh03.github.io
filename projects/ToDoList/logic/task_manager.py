import json
import os
from datetime import datetime

class TaskManager:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = {}
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.tasks = json.load(f)
        else:
            self.tasks = {}

    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self, title, due_date, tag, description, repeat=False):
        task = {
            'title': title,
            'description': description,
            'tag': tag,
            'repeat': repeat,
            'complete': False,
            'due': due_date,
            'start': '',
            'end': '',
            'completed_dates': []
        }
        if due_date not in self.tasks:
            self.tasks[due_date] = []
        self.tasks[due_date].append(task)
        self.save_tasks()

    def get_tasks_by_date(self, date):
        return self.tasks.get(date, [])

    def set_task_completion(self, date, title, complete):
        if date in self.tasks:
            for task in self.tasks[date]:
                if task['title'] == title:
                    task['complete'] = complete
                    if complete and task['repeat']:
                        if 'completed_dates' not in task:
                            task['completed_dates'] = []
                        task['completed_dates'].append(date)
                    break
        self.save_tasks()

    def delete_task(self, date, title):
        if date in self.tasks:
            self.tasks[date] = [task for task in self.tasks[date] if task['title'] != title]
            if not self.tasks[date]:
                del self.tasks[date]
            self.save_tasks()

    def get_completed_tasks(self):
        completed = []
        for date, task_list in self.tasks.items():
            for task in task_list:
                if task['repeat'] and date in task.get('completed_dates', []):
                    task_copy = task.copy()
                    task_copy['due'] = date
                    completed.append(task_copy)
                elif not task['repeat'] and task['complete']:
                    task_copy = task.copy()
                    task_copy['due'] = date
                    completed.append(task_copy)
        return completed
