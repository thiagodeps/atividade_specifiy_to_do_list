"""Task model for Zentask."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from enum import Enum
import uuid

class TaskStatus(str, Enum):
    """Allowed task states per feature spec."""
    TO_DO = "to_do"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    PAUSED = "paused"

@dataclass(frozen=False)
class Task:
    """
    Task representation.

    All timestamps in ISO 8601 format (UTC).
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TO_DO
    due_date: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    pause_reason: Optional[str] = None

    def __post_init__(self):
        """Validation on creation."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")

        if self.due_date and not self._is_valid_iso_date(self.due_date):
            raise ValueError(f"due_date must be ISO 8601 format: {self.due_date}")

    @staticmethod
    def _is_valid_iso_date(date_str: str) -> bool:
        """Validate YYYY-MM-DD format."""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def to_dict(self) -> dict:
        """Serialize to dict for JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "due_date": self.due_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "pause_reason": self.pause_reason,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Deserialize from dict."""
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description"),
            status=TaskStatus(data["status"]),
            due_date=data.get("due_date"),
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            pause_reason=data.get("pause_reason"),
        )