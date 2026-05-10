"""JSON tasks persistence for Zentask."""

import json
from pathlib import Path
from typing import Dict

from ..models.task import Task
from ..config import TASKS_FILE

class JsonTasksPersistence:
    """Handles tasks persistence using JSON format."""

    def __init__(self, tasks_file: Path = TASKS_FILE):
        self.tasks_file = tasks_file
        self.tasks_file.parent.mkdir(exist_ok=True)

    def save_tasks(self, tasks: Dict[str, Task]) -> None:
        """Save all tasks to the JSON file."""
        data = {task_id: task.to_dict() for task_id, task in tasks.items()}
        with open(self.tasks_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_tasks(self) -> Dict[str, Task]:
        """Load all tasks from the JSON file."""
        if not self.tasks_file.exists():
            return {}

        try:
            with open(self.tasks_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {task_id: Task.from_dict(task_data) for task_id, task_data in data.items()}
        except (json.JSONDecodeError, FileNotFoundError):
            # Return empty dict if file is corrupted or doesn't exist
            return {}