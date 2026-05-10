"""JSON Lines audit log persistence for Zentask."""

import json
from pathlib import Path
from typing import List
from datetime import datetime

from ..models.audit_event import AuditEvent
from ..config import AUDIT_LOG_FILE

class JsonLogPersistence:
    """Handles audit log persistence using JSON Lines format."""

    def __init__(self, log_file: Path = AUDIT_LOG_FILE):
        self.log_file = log_file
        self.log_file.parent.mkdir(exist_ok=True)

    def append_event(self, event: AuditEvent) -> None:
        """Append an audit event to the log file."""
        with open(self.log_file, "a", encoding="utf-8") as f:
            json.dump(event.to_dict(), f, ensure_ascii=False)
            f.write("\n")

    def get_all_events(self) -> List[AuditEvent]:
        """Retrieve all audit events from the log file."""
        events = []
        if not self.log_file.exists():
            return events

        with open(self.log_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        data = json.loads(line)
                        events.append(AuditEvent.from_dict(data))
                    except (json.JSONDecodeError, KeyError):
                        # Skip malformed lines
                        continue
        return events

    def get_events_for_task(self, task_id: str) -> List[AuditEvent]:
        """Get all audit events for a specific task."""
        return [event for event in self.get_all_events() if event.task_id == task_id]