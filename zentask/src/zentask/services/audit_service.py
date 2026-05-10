"""Audit service for Zentask."""

from datetime import datetime, timezone
from typing import List

from ..models.audit_event import AuditEvent
from ..persistence.json_log import JsonLogPersistence

class AuditService:
    """Handles audit logging and retrieval."""

    def __init__(self, persistence: JsonLogPersistence = None):
        self.persistence = persistence or JsonLogPersistence()

    def log_event(self, user_id: str, action: str, task_id: str, details: dict = None) -> AuditEvent:
        """Log an audit event."""
        event = AuditEvent(
            timestamp=datetime.now(timezone.utc).isoformat(),
            user_id=user_id,
            action=action,
            task_id=task_id,
            details=details or {}
        )
        self.persistence.append_event(event)
        return event

    def get_all_events(self) -> List[AuditEvent]:
        """Get all audit events."""
        return self.persistence.get_all_events()

    def get_events_for_task(self, task_id: str) -> List[AuditEvent]:
        """Get audit events for a specific task."""
        return self.persistence.get_events_for_task(task_id)