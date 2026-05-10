"""Task service for Zentask."""

from datetime import datetime, timezone
from typing import List, Optional, Dict
from dataclasses import replace

from ..models.task import Task, TaskStatus
from ..services.audit_service import AuditService
from ..persistence.json_tasks import JsonTasksPersistence
from ..config import MAX_TITLE_LENGTH, MAX_DESCRIPTION_LENGTH

class TaskService:
    """Handles all task CRUD operations and state transitions."""

    def __init__(self, audit_service: AuditService = None):
        self.audit_service = audit_service or AuditService()
        self.persistence = JsonTasksPersistence()
        self.tasks: Dict[str, Task] = self.persistence.load_tasks()

    def _save_tasks(self):
        """Save current tasks to persistent storage."""
        self.persistence.save_tasks(self.tasks)

    def create(self, title: str, description: Optional[str] = None, due_date: Optional[str] = None) -> Task:
        """Create a new task."""
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        if len(title) > MAX_TITLE_LENGTH:
            raise ValueError(f"Title too long (max {MAX_TITLE_LENGTH} characters)")

        if description and len(description) > MAX_DESCRIPTION_LENGTH:
            raise ValueError(f"Description too long (max {MAX_DESCRIPTION_LENGTH} characters)")

        task = Task(
            title=title.strip(),
            description=description.strip() if description else None,
            due_date=due_date
        )

        self.tasks[task.id] = task
        self.audit_service.log_event("system", "create", task.id, {"title": task.title})
        self._save_tasks()
        return task

    def get(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by ID."""
        return self.tasks.get(task_id)

    def list(self, status_filter: Optional[TaskStatus] = None) -> List[Task]:
        """Retrieve all tasks, optionally filtered by status."""
        tasks = list(self.tasks.values())
        if status_filter:
            tasks = [t for t in tasks if t.status == status_filter]
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)

    def update(self, task_id: str, title: Optional[str] = None, description: Optional[str] = None,
               due_date: Optional[str] = None) -> Task:
        """Update task title, description, or due date."""
        task = self.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        updates = {}
        if title is not None:
            if not title.strip():
                raise ValueError("Task title cannot be empty")
            if len(title) > MAX_TITLE_LENGTH:
                raise ValueError(f"Title too long (max {MAX_TITLE_LENGTH} characters)")
            updates["title"] = title.strip()

        if description is not None:
            if len(description) > MAX_DESCRIPTION_LENGTH:
                raise ValueError(f"Description too long (max {MAX_DESCRIPTION_LENGTH} characters)")
            updates["description"] = description.strip() if description else None

        if due_date is not None:
            # Validate date format
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"due_date must be ISO 8601 format: {due_date}")
            updates["due_date"] = due_date

        if updates:
            updated_task = replace(task, updated_at=datetime.now(timezone.utc).isoformat(), **updates)
            self.tasks[task_id] = updated_task
            self.audit_service.log_event("system", "update", task_id, updates)
            self._save_tasks()
            return updated_task

        return task

    def change_status(self, task_id: str, new_status: TaskStatus, reason: Optional[str] = None) -> Task:
        """Transition task to a new status."""
        task = self.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        updates = {"status": new_status}
        if new_status == TaskStatus.PAUSED and reason:
            updates["pause_reason"] = reason

        updated_task = replace(task, updated_at=datetime.now(timezone.utc).isoformat(), **updates)
        self.tasks[task_id] = updated_task

        details = {"new_status": new_status.value}
        if reason:
            details["reason"] = reason
        self.audit_service.log_event("system", "status_change", task_id, details)
        self._save_tasks()

        return updated_task

    def defer(self, task_id: str, new_due_date: str) -> Task:
        """Postpone a task to a future date."""
        # Validate date format
        try:
            datetime.strptime(new_due_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"new_due_date must be ISO 8601 format: {new_due_date}")

        return self.update(task_id, due_date=new_due_date)

    def delete(self, task_id: str) -> bool:
        """Soft-delete a task."""
        task = self.tasks.pop(task_id, None)
        if task:
            self.audit_service.log_event("system", "delete", task_id, {"title": task.title})
            self._save_tasks()
            return True
        return False