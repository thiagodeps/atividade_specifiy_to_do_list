"""Audit event model for Zentask."""

from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class AuditEvent:
    """
    Immutable event log entry. No updates after creation; only new events appended.
    """
    timestamp: str
    user_id: str
    action: str
    task_id: str
    details: dict = None

    def to_dict(self) -> dict:
        """Serialize to dict for JSON."""
        return {
            "timestamp": self.timestamp,
            "user_id": self.user_id,
            "action": self.action,
            "task_id": self.task_id,
            "details": self.details or {},
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AuditEvent":
        """Deserialize from dict."""
        return cls(
            timestamp=data["timestamp"],
            user_id=data["user_id"],
            action=data["action"],
            task_id=data["task_id"],
            details=data.get("details", {}),
        )