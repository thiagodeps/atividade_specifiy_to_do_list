# Data Model: Task Lifecycle Management

**Date**: 2026-05-09  
**Phase**: Phase 1 - Design & Contracts  
**Status**: Design specification (pre-implementation)

## Entity Definitions

### Task

Represents a single to-do item with full lifecycle state.

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum

class TaskStatus(str, Enum):
    """Allowed task states per feature spec."""
    TO_DO = "to_do"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    PAUSED = "paused"

@dataclass(frozen=False)
class Task:
    """
    Immutable task representation (use replace() to update).
    
    All timestamps in ISO 8601 format (UTC).
    """
    id: str                           # Unique identifier (UUID or timestamp-based)
    title: str                        # Required; non-empty string
    description: Optional[str] = None # Optional; can be empty string
    status: TaskStatus = TaskStatus.TO_DO
    due_date: Optional[str] = None    # ISO 8601 date format (YYYY-MM-DD)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    pause_reason: Optional[str] = None # Capture why task is paused (e.g., "Waiting for approval")
    
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
            from datetime import datetime as dt
            dt.strptime(date_str, "%Y-%m-%d")
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
```

**Constraints**:
- `title`: Non-empty, max 500 characters
- `description`: Optional, max 2000 characters
- `due_date`: Optional, ISO 8601 format (YYYY-MM-DD), can be past date
- `status`: One of {TO_DO, IN_PROGRESS, DONE, PAUSED}
- `pause_reason`: Only meaningful when status == PAUSED; optional even then

**Relationships**:
- One Task can have many AuditEvents (1:N)
- No cross-task dependencies (blocked relationships recorded via pause_reason text)

---

### AuditEvent

Immutable record of task mutations; forms append-only event log.

```python
@dataclass(frozen=True)  # Frozen: truly immutable
class AuditEvent:
    """
    Immutable event log entry. No updates after creation; only new events appended.
    """
    timestamp: str                    # ISO 8601 timestamp (UTC)
    user_id: str                      # "system" for single-user app
    action: str                       # Enum: create | update | delete | status_change | defer | pause
    task_id: str                      # Task affected
    before_state: Optional[dict] = None  # Task state before action (None for create)
    after_state: dict                 # Task state after action
    reason: Optional[str] = None      # Why user made change (optional)
    
    def to_dict(self) -> dict:
        """Serialize to dict for JSON Lines."""
        return {
            "timestamp": self.timestamp,
            "user_id": self.user_id,
            "action": self.action,
            "task_id": self.task_id,
            "before_state": self.before_state,
            "after_state": self.after_state,
            "reason": self.reason,
        }
```

**Event Actions**:
- `create`: New task created
- `update`: Title, description, due_date changed (not status)
- `status_change`: Status transitioned (TO_DO ↔ IN_PROGRESS ↔ DONE ↔ PAUSED)
- `delete`: Task deleted (soft-delete; entry in audit log)
- `defer`: Task due date postponed
- `pause`: Task status set to PAUSED with optional reason

**Constraints**:
- Immutable after creation (frozen dataclass)
- `timestamp` in UTC ISO 8601 format
- `before_state` null for `create` action; present for all others
- `action` from enum of allowed values

---

### Status Transitions

Valid state machine for task status:

```
         ┌─────────────────────────────────┐
         │                                  │
    ┌────▼──────┐       ┌─────────────┐    │
    │  TO_DO    ◄──────►│ IN_PROGRESS ├────┤
    └────▲──────┘       └─────┬───────┘    │
         │                    │             │
         │                    ▼             │
         │               ┌─────────┐        │
         │               │  DONE   ┼────────┤
         │               └─────────┘        │
         │                                  │
         │          ┌──────────────┐        │
         └─────────►│   PAUSED     ├────────┘
                    └──────────────┘
```

**Transition Rules**:
- TO_DO ↔ IN_PROGRESS: Direct transition
- IN_PROGRESS → DONE: Direct transition
- DONE → TO_DO: Allowed (undo completion)
- DONE → IN_PROGRESS: Allowed (resume before finalizing)
- Any status → PAUSED: Transition from any state to paused
- PAUSED → previous status: Transition back to any state
- No state prevents another transition (reversible workflow)

---

## Data Validation Rules

| Field | Rule | Example |
|-------|------|---------|
| `task.title` | Non-empty, trim whitespace | `"  "` → ValueError |
| `task.description` | Optional; allow empty string | `""` or `None` allowed |
| `task.due_date` | ISO 8601 (YYYY-MM-DD) or None | `"2026-05-15"` valid; `"5/15/26"` invalid |
| `task.status` | One of {TO_DO, IN_PROGRESS, DONE, PAUSED} | Enum enforced |
| `task.pause_reason` | Meaningful only when status=PAUSED | Can be None or free text |
| `audit_event.timestamp` | ISO 8601 UTC | Auto-generated by service layer |
| `audit_event.action` | {create, update, delete, status_change, defer, pause} | Enum enforced |
| `audit_event.before_state` | None for create; Task.to_dict() for others | Validated by service |

---

## State Transition Examples

### Example 1: Create → In Progress → Done

```json
// Event 1: Create
{
  "timestamp": "2026-05-09T10:00:00Z",
  "action": "create",
  "task_id": "task-001",
  "before_state": null,
  "after_state": {
    "id": "task-001",
    "title": "Buy groceries",
    "description": null,
    "status": "to_do",
    "due_date": "2026-05-10",
    "created_at": "2026-05-09T10:00:00Z",
    "updated_at": "2026-05-09T10:00:00Z",
    "pause_reason": null
  },
  "reason": null
}

// Event 2: Status change (TO_DO → IN_PROGRESS)
{
  "timestamp": "2026-05-09T10:15:00Z",
  "action": "status_change",
  "task_id": "task-001",
  "before_state": { "status": "to_do", ... },
  "after_state": { "status": "in_progress", ... },
  "reason": null
}

// Event 3: Status change (IN_PROGRESS → DONE)
{
  "timestamp": "2026-05-09T11:00:00Z",
  "action": "status_change",
  "task_id": "task-001",
  "before_state": { "status": "in_progress", ... },
  "after_state": { "status": "done", ... },
  "reason": null
}
```

### Example 2: Defer + Pause

```json
// Event 1: Defer (due date change)
{
  "timestamp": "2026-05-09T14:00:00Z",
  "action": "defer",
  "task_id": "task-002",
  "before_state": { "due_date": "2026-05-10", "status": "in_progress", ... },
  "after_state": { "due_date": "2026-05-15", "status": "in_progress", ... },
  "reason": "Not ready yet, need approval"
}

// Event 2: Pause (status change to PAUSED)
{
  "timestamp": "2026-05-09T14:05:00Z",
  "action": "pause",
  "task_id": "task-002",
  "before_state": { "status": "in_progress", "pause_reason": null, ... },
  "after_state": { "status": "paused", "pause_reason": "Waiting for approval from John", ... },
  "reason": "Blocked by dependency"
}
```

---

## Key Entities Summary

| Entity | Purpose | Mutable | Persistence |
|--------|---------|---------|-------------|
| Task | Current state of a to-do item | Yes (via service layer) | In-memory dict |
| AuditEvent | Immutable record of what changed | No (frozen) | JSON Lines file |
| TaskStatus | Enum of allowed states | No | Code-level constant |

---

## Next Steps

1. Implement models in `src/zentask/models/task.py` and `src/zentask/models/audit_event.py`
2. Implement services in `src/zentask/services/task_service.py` (handles state transitions + audit creation)
3. Implement persistence in `src/zentask/persistence/json_log.py` (append AuditEvent to file)
