# Service Contracts: Task Lifecycle Management

**Date**: 2026-05-09  
**Phase**: Phase 1 - Interface Contracts  

## Overview

This document defines the public interfaces (contracts) for the business logic layer. These contracts are language-agnostic and define what inputs/outputs each service expects.

---

## TaskService Contract

Handles all task CRUD operations and state transitions. Implemented in `src/zentask/services/task_service.py`.

### Methods

#### `create(title: str, description: str | None, due_date: str | None) -> Task`

**Purpose**: Create a new task.

**Inputs**:
- `title` (string, required): Task title; must be non-empty after trim
- `description` (string, optional): Task description
- `due_date` (ISO 8601 date string, optional): Due date in YYYY-MM-DD format

**Output**: Newly created Task object with:
- Generated `id` (UUID or timestamp-based)
- `status` = `TO_DO`
- `created_at` and `updated_at` set to current timestamp

**Side Effects**:
- Logs AuditEvent with action=`create` to audit service
- Task added to in-memory store

**Errors**:
- Raises `ValueError` if title is empty/whitespace
- Raises `ValueError` if due_date invalid ISO 8601 format

**Example**:
```python
task = task_service.create(
    title="Buy groceries",
    description="Milk, bread, eggs",
    due_date="2026-05-15"
)
# Returns Task(id="task-001", title="Buy groceries", status="to_do", ...)
```

---

#### `get(task_id: str) -> Task | None`

**Purpose**: Retrieve a task by ID.

**Inputs**:
- `task_id` (string): Task identifier

**Output**: Task object or `None` if not found

**Side Effects**: None

**Errors**: None (returns None on not found)

---

#### `list(status_filter: TaskStatus | None = None) -> List[Task]`

**Purpose**: Retrieve all tasks, optionally filtered by status.

**Inputs**:
- `status_filter` (TaskStatus enum, optional): Filter by status; if None, return all

**Output**: List of Task objects (empty list if no matches)

**Side Effects**: None

**Errors**: None

**Example**:
```python
# Get all tasks
all_tasks = task_service.list()

# Get only in-progress tasks
in_progress = task_service.list(status_filter=TaskStatus.IN_PROGRESS)
```

---

#### `update(task_id: str, title: str | None = None, description: str | None = None, due_date: str | None = None) -> Task`

**Purpose**: Update task title, description, or due date (not status; see `change_status` for that).

**Inputs**:
- `task_id` (string): Task to update
- `title` (string, optional): New title (if provided, must be non-empty)
- `description` (string, optional): New description
- `due_date` (ISO 8601 string, optional): New due date

**Output**: Updated Task object

**Side Effects**:
- Updates task in in-memory store
- Sets `updated_at` to current timestamp
- Logs AuditEvent with action=`update`

**Errors**:
- Raises `ValueError` if task not found
- Raises `ValueError` if new title empty/whitespace
- Raises `ValueError` if due_date invalid format

---

#### `change_status(task_id: str, new_status: TaskStatus, reason: str | None = None) -> Task`

**Purpose**: Transition task to a new status (supports reversible state machine).

**Inputs**:
- `task_id` (string): Task to update
- `new_status` (TaskStatus enum): Target status (TO_DO | IN_PROGRESS | DONE | PAUSED)
- `reason` (string, optional): Explanation for status change

**Output**: Updated Task object with new status

**Side Effects**:
- Updates task status in in-memory store
- Sets `updated_at` to current timestamp
- Logs AuditEvent with action=`status_change`
- If new_status=PAUSED and reason provided, sets `pause_reason` field

**Errors**:
- Raises `ValueError` if task not found
- Raises `ValueError` if new_status not a valid TaskStatus enum

**Validation**:
- All state transitions allowed (fully reversible per feature spec)

**Example**:
```python
task = task_service.change_status(
    task_id="task-001",
    new_status=TaskStatus.IN_PROGRESS,
    reason="Started working"
)
# Task.status → IN_PROGRESS

task = task_service.change_status(
    task_id="task-001",
    new_status=TaskStatus.PAUSED,
    reason="Waiting for approval from John"
)
# Task.status → PAUSED
# Task.pause_reason → "Waiting for approval from John"
```

---

#### `defer(task_id: str, new_due_date: str) -> Task`

**Purpose**: Postpone a task to a future date (special case of update).

**Inputs**:
- `task_id` (string): Task to defer
- `new_due_date` (ISO 8601 string): New due date (must be ISO 8601 YYYY-MM-DD)

**Output**: Updated Task object with new due_date

**Side Effects**:
- Updates task due_date
- Sets `updated_at` to current timestamp
- Logs AuditEvent with action=`defer`

**Errors**:
- Raises `ValueError` if task not found
- Raises `ValueError` if new_due_date invalid format

**Example**:
```python
task = task_service.defer(
    task_id="task-001",
    new_due_date="2026-05-20"
)
# Task.due_date → "2026-05-20"
```

---

#### `delete(task_id: str) -> bool`

**Purpose**: Soft-delete a task (removes from active view, logs in audit trail).

**Inputs**:
- `task_id` (string): Task to delete

**Output**: `True` if deleted; `False` if task not found

**Side Effects**:
- Removes task from in-memory store
- Logs AuditEvent with action=`delete` (audit log retains record)
- UI shows undo button with 10-second window

**Errors**: None (returns False on not found)

**Note**: User can restore within 10 seconds via `undo_delete()`. After timeout, task is permanently lost (but audit log persists).

---

#### `undo_delete(task_id: str, previous_state: dict) -> Task`

**Purpose**: Restore a task deleted within the undo window.

**Inputs**:
- `task_id` (string): Task to restore
- `previous_state` (dict): Task state before deletion (captured at deletion time)

**Output**: Restored Task object

**Side Effects**:
- Re-adds task to in-memory store
- Logs AuditEvent with action=`create` (indicates restoration)

**Errors**: None (if task already exists, overwrites)

---

## AuditService Contract

Handles all audit event logging and retrieval. Implemented in `src/zentask/services/audit_service.py`.

### Methods

#### `log_event(action: str, task_id: str, before_state: dict | None, after_state: dict, reason: str | None = None) -> AuditEvent`

**Purpose**: Log a task mutation event.

**Inputs**:
- `action` (string): Action type (create | update | delete | status_change | defer | pause)
- `task_id` (string): Task affected
- `before_state` (dict, optional): Task state before action (None for create)
- `after_state` (dict): Task state after action (always present)
- `reason` (string, optional): Why the action was taken

**Output**: AuditEvent object (newly created and persisted)

**Side Effects**:
- Appends AuditEvent to JSON Lines audit log file
- Event is immutable once written

**Errors**:
- Raises `IOError` if audit log file cannot be written
- Raises `ValueError` if action not in enum

**Internal**:
- Auto-generates `timestamp` (UTC ISO 8601)
- Sets `user_id` to "system" (single-user app)

**Example**:
```python
event = audit_service.log_event(
    action="status_change",
    task_id="task-001",
    before_state={"status": "to_do", ...},
    after_state={"status": "in_progress", ...},
    reason="User started working"
)
```

---

#### `get_events(task_id: str | None = None, action_filter: str | None = None) -> List[AuditEvent]`

**Purpose**: Retrieve audit events, optionally filtered by task or action.

**Inputs**:
- `task_id` (string, optional): Filter events for specific task; if None, return all
- `action_filter` (string, optional): Filter events by action type; if None, return all actions

**Output**: List of AuditEvent objects (empty list if no matches)

**Side Effects**: None

**Errors**: None

**Example**:
```python
# All events for task-001
events = audit_service.get_events(task_id="task-001")

# All status_change events
status_changes = audit_service.get_events(action_filter="status_change")

# status_change events for task-001
task_status_history = audit_service.get_events(
    task_id="task-001",
    action_filter="status_change"
)
```

---

#### `export_audit_log() -> str`

**Purpose**: Export full audit trail as JSON Lines string (for user download/backup).

**Inputs**: None

**Output**: Multi-line string where each line is a JSON object (JSON Lines format)

**Side Effects**: None

**Errors**:
- Raises `IOError` if audit log file cannot be read

**Example**:
```python
audit_log_text = audit_service.export_audit_log()
# Returns:
# {"timestamp": "...", "action": "create", ...}
# {"timestamp": "...", "action": "status_change", ...}
```

---

#### `clear_audit_log() -> bool`

**Purpose**: Delete audit log (user privacy control per Constitution IV).

**Inputs**: None

**Output**: `True` if cleared; `False` if file not found or already empty

**Side Effects**:
- Deletes audit log file (if exists)
- All history lost

**Errors**: Raises `IOError` if file exists but cannot be deleted

**Note**: Per Constitution, user must explicitly request this; no automatic cleanup.

---

## State Representation

### Task State (as dict)

Used in `before_state` and `after_state` fields of AuditEvent:

```python
{
    "id": "task-001",
    "title": "Buy groceries",
    "description": "Milk, bread, eggs",
    "status": "in_progress",
    "due_date": "2026-05-15",
    "created_at": "2026-05-09T10:00:00Z",
    "updated_at": "2026-05-09T10:15:00Z",
    "pause_reason": None
}
```

---

## Error Handling Strategy

All services raise explicit error types (no generic `Exception`):

- `ValueError`: Invalid input (empty title, invalid date, invalid enum value)
- `IOError`: File I/O failures (audit log write, read)
- `KeyError`: Task not found (only if accessed directly; `list()` and `get()` return empty/None)

Callers must handle these explicitly:

```python
try:
    task = task_service.create(title="")
except ValueError as e:
    ui.show_error(f"Invalid task: {e}")
```

---

## Performance Expectations

| Operation | Time Complexity | Expected Runtime |
|-----------|-----------------|-----------------|
| `create()` | O(1) | < 10ms (dict insert + audit log write) |
| `get()` | O(1) | < 1ms (dict lookup) |
| `list()` | O(n) | < 50ms for 1000 tasks |
| `update()` | O(1) | < 10ms |
| `change_status()` | O(1) | < 10ms |
| `defer()` | O(1) | < 10ms |
| `delete()` | O(1) | < 10ms |
| `log_event()` | O(1) amortized | < 10ms (append to file) |
| `get_events()` | O(n) | < 100ms for 1000 events |

*Note: Includes in-memory operations + audit log file I/O*

---

## Thread Safety

**Current Implementation**: Single-threaded (Streamlit runs in single thread per session).

**Future Consideration**: If multi-user support added, TaskService and AuditService must use locks for concurrent access to in-memory dict and audit log file.

---

## Next Steps

1. Implement TaskService and AuditService per these contracts
2. Create tests verifying each method matches contract
3. Integration tests verify service interaction (create → change_status → log)
