# Feature Specification: Task Lifecycle Management

**Feature Branch**: `001-task-lifecycle-management`  
**Created**: 2026-05-09  
**Status**: Draft  
**Input**: User description: "quero poder registrar tarefas, quero poder marca como em andamento ou concluido, quero editar ou excuir tarefas, quero poder adiar taferas ou colocar eles como indertemidao/em pausa"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create a New Task (Priority: P1)

A user wants to quickly register a new task to capture ideas, todos, and responsibilities. This is the foundation of the task management system - without task creation, nothing else is possible.

**Why this priority**: P1 is critical for MVP. Users cannot use the app without being able to create tasks. This is the entry point to all task management features.

**Independent Test**: Can be fully tested by opening the app, creating a task with a title, and verifying it appears in the task list. Delivers immediate value.

**Acceptance Scenarios**:

1. **Given** user is in the task list view, **When** user creates a new task with title "Buy groceries", **Then** task appears in the list with "To Do" status
2. **Given** a task has been created, **When** user views the list, **Then** task is displayed with creation date and default status
3. **Given** user attempts to create a task without a title, **When** user tries to save, **Then** system shows validation error and prevents creation

---

### User Story 2 - Update Task Status (In Progress / Done) (Priority: P1)

A user wants to track task progress by transitioning tasks between statuses: "To Do" → "In Progress" → "Done". This provides immediate feedback on what they're working on.

**Why this priority**: P1 is critical for task tracking. Without status updates, users cannot show progress or organize their work. This directly supports anti-anxiety focus (clear today/in-progress/done separation).

**Independent Test**: Can be tested independently by creating a task, toggling it to "In Progress", then to "Done", and verifying status changes persist. Provides core workflow value.

**Acceptance Scenarios**:

1. **Given** task has status "To Do", **When** user marks it as "In Progress", **Then** status updates immediately in the list and persists
2. **Given** task has status "In Progress", **When** user marks it as "Done", **Then** status updates to "Done" and task may be moved to completed section
3. **Given** task has status "Done", **When** user marks it back to "To Do", **Then** status reverts and task reappears in active list
4. **Given** multiple tasks exist in different statuses, **When** user views the list, **Then** tasks are grouped by status or clearly marked with status badges

---

### User Story 3 - Edit Task Details (Priority: P1)

A user wants to modify task information (title, description, due date) after creation without losing the task history or audit trail.

**Why this priority**: P1 supports real-world task management. Tasks evolve, deadlines change, and users need to update context. Aligns with audit trail principle (IV) - changes are tracked.

**Independent Test**: Can be tested by creating a task, editing its title/description, and verifying changes are saved and reflected in the list. Supports long-term task management.

**Acceptance Scenarios**:

1. **Given** task "Buy groceries" exists, **When** user edits title to "Buy groceries and cook dinner", **Then** title updates immediately
2. **Given** task has no description, **When** user adds description "Need: milk, bread, eggs", **Then** description is saved and displayed
3. **Given** task has a due date, **When** user changes due date to next week, **Then** due date updates and task list reflects change
4. **Given** task is edited, **When** audit log is checked, **Then** edit event shows timestamp, old value, new value, and reason (if provided)

---

### User Story 4 - Delete or Archive Tasks (Priority: P2)

A user wants to remove tasks from the active list either by permanent deletion (with confirmation) or soft-delete/archive to keep audit trail intact.

**Why this priority**: P2 provides cleanup capability. Users need to remove completed or irrelevant tasks. Supports audit trail principle - deletion is logged, not erased.

**Independent Test**: Can be tested by creating a task, deleting it, and verifying it no longer appears in the active list (but audit log retains record). Supports list hygiene.

**Acceptance Scenarios**:

1. **Given** task "Old task" exists, **When** user deletes it, **Then** system shows undo prompt (10-second window), and task can be restored
2. **Given** task is deleted and 11 seconds pass, **When** user views task list, **Then** task no longer appears in active view
3. **Given** task is deleted, **When** user exports audit trail, **Then** deletion event is recorded with timestamp and user who deleted it
4. **Given** user deletes task by mistake, **When** user clicks undo within 10 seconds, **Then** task is restored to previous status

---

### User Story 5 - Defer / Postpone Tasks (Priority: P2)

A user wants to move tasks to a later date without deleting them. This helps manage today's focus by hiding future tasks. Supports anti-anxiety principle (III) - today's view shows only today's work.

**Why this priority**: P2 enhances focus and reduces cognitive load. Deferring tasks separates today's work from future planning, reducing overwhelm.

**Independent Test**: Can be tested by creating a task due today, deferring it to tomorrow, and verifying it disappears from today's view and reappears tomorrow. Supports focus principle.

**Acceptance Scenarios**:

1. **Given** task "Call dentist" is due today, **When** user defers it to May 15, **Then** task disappears from today's view and reappears on May 15
2. **Given** task is deferred, **When** user views future tasks, **Then** deferred task is visible with new due date
3. **Given** task is deferred, **When** user views audit trail, **Then** deferral event shows original date, new date, and timestamp
4. **Given** multiple tasks are due today, **When** user defers one, **Then** only the deferred task moves; others remain in today's view

---

### User Story 6 - Pause / Mark as Indeterminate (Priority: P2)

A user wants to temporarily suspend a task without deleting it - marking it as "Paused" or "Blocked" when it depends on external factors (waiting for feedback, blocked by another task, etc.).

**Why this priority**: P2 supports realistic task management. Tasks often become stuck waiting for dependencies. Paused status prevents false urgency and reduces anxiety about "stuck" work.

**Independent Test**: Can be tested by creating an "In Progress" task, marking it as "Paused", and verifying it no longer appears in active/today view. Supports workflow clarity.

**Acceptance Scenarios**:

1. **Given** task is "In Progress", **When** user marks it as "Paused", **Then** status changes to "Paused" and reason can be logged (e.g., "Waiting for approval")
2. **Given** task has status "Paused", **When** user views the today/active list, **Then** paused task is hidden or marked separately (not in active flow)
3. **Given** task is paused, **When** reason is provided (e.g., "Blocked by TASK-123"), **Then** reason is stored in audit trail
4. **Given** paused task is unblocked, **When** user marks it "In Progress" again, **Then** status resumes and task reappears in active list

---

### Edge Cases

- What happens if a user creates a task with empty title? → Validation error; task not saved
- What happens if user edits a task's due date to a past date? → System allows it but shows warning; task may appear in overdue section
- What happens if undo window (10s) expires after deletion? → Task becomes permanently deleted; audit log retains record
- What happens if user defers a paused task? → Paused task moves to deferred date; status remains paused
- What happens if user tries to edit a task while it's being synced? → Optimistic update on client; sync conflict resolved per audit trail principle
- What happens if task is paused but reason is not provided? → Status updates without reason; reason can be added later via edit

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to create tasks with at minimum a title (description, due date optional)
- **FR-002**: System MUST validate that task title is not empty before saving
- **FR-003**: System MUST allow users to update task status between: "To Do", "In Progress", "Done" with single-click/keyboard action
- **FR-004**: System MUST allow status transitions: To Do ↔ In Progress ↔ Done (and reversible to previous state)
- **FR-005**: System MUST display status change immediately in the UI (sub-100ms per Constitution II)
- **FR-006**: System MUST allow users to edit task title, description, and due date after creation
- **FR-007**: System MUST persist all task edits with timestamp and audit trail entry
- **FR-008**: System MUST allow users to delete tasks with 10-second undo window before permanent deletion
- **FR-009**: System MUST log all deletions in audit trail (no data loss, only soft-delete in active view)
- **FR-010**: System MUST allow users to defer/postpone tasks to a specific future date
- **FR-011**: System MUST remove deferred tasks from today's view and show them on their new due date
- **FR-012**: System MUST allow users to pause tasks and optionally provide a reason (e.g., "Waiting for", "Blocked by")
- **FR-013**: System MUST hide paused tasks from active/today view (not deleted, just suppressed from active list)
- **FR-014**: System MUST support "Paused" as a distinct status separate from "To Do", "In Progress", "Done"
- **FR-015**: System MUST log task state transitions with: timestamp, old status, new status, user, and reason (if applicable)
- **FR-016**: System MUST support keyboard-only workflow: task creation, status updates, deferral, pause (per Constitution I)
- **FR-017**: System MUST prevent double-submission of task changes via optimistic updates + race-condition guards (per Constitution II)

### Non-Functional Requirements

- **NFR-001**: Task status changes MUST be acknowledged in UI within 100ms (per Constitution II - Instant Feedback)
- **NFR-002**: All task mutations (create, update, delete, status change) MUST be recorded in immutable audit log with event structure: {timestamp_iso, user_id, action, task_id, before_state, after_state, reason}
- **NFR-003**: Audit trail MUST be stored locally first, cloud sync secondary (per Constitution IV)
- **NFR-004**: No task information MUST be silently lost; deletion is soft-delete with audit trail entry (per Constitution VI - Anti-Patterns)

### Key Entities

- **Task**: Represents a single to-do item
  - Attributes: `id` (unique), `title` (string, required), `description` (string, optional), `status` (enum: To Do | In Progress | Done | Paused), `due_date` (date, optional), `created_at` (timestamp), `updated_at` (timestamp)
  
- **Task Status**: Enumeration of allowed task states
  - Values: `to_do`, `in_progress`, `done`, `paused`
  
- **Audit Event**: Immutable record of task mutations
  - Attributes: `timestamp` (ISO 8601), `user_id` (string), `action` (enum: create | update | delete | status_change | defer | pause), `task_id` (string), `before_state` (object), `after_state` (object), `reason` (string, optional)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001 - Task Creation**: User can create a task with title in < 5 seconds using keyboard or mouse
- **SC-002 - Status Transitions**: Status change from To Do → In Progress → Done is visible on screen within 100ms
- **SC-003 - Today's View**: Today's view shows only tasks due today + overdue; future deferred tasks are hidden
- **SC-004 - Undo Window**: Deleted tasks can be restored within 10 seconds; after 10 seconds, delete is final
- **SC-005 - Audit Trail**: Every task mutation appears in audit log with complete before/after state within 1 second of mutation
- **SC-006 - Keyboard Accessibility**: All core actions (create, status update, defer, pause) executable via keyboard hotkeys defined in Constitution I
- **SC-007 - No Silent Failures**: All task mutations are either confirmed in UI (success toast) or show error message within 500ms

### User Experience Metrics

- **SC-008 - Instant Feedback**: User perceives action "completed" - optimistic update shows immediately; no loading spinner unless operation > 200ms
- **SC-009 - Focus Clarity**: User can distinguish between today's tasks, future tasks, and paused tasks at a glance
- **SC-010 - Mistake Recovery**: User accidentally deletes task and can undo within 10-second window
- **SC-011 - Workflow Efficiency**: Core task workflow (create → update status → defer/pause) requires no modal dialogs (direct inline actions)

## Assumptions

- Users have single-user access (no multi-user conflict resolution complexity in V1)
- Due dates are day-level precision (not time-of-day)
- "Paused" reason is optional; system allows pause without reason provided
- Audit trail retention is indefinite (per Constitution IV); user can export/delete history via privacy control
- Today's view shows tasks due "today" (current date) and tasks with past due dates (overdue section)
- Deferral moves task to a future date; deferred task retains previous status (e.g., if paused, remains paused on new date)

## Out of Scope

- Multi-user collaboration, task assignment to others, permissions
- Recurring tasks or templates
- Sub-tasks (captured in Constitution principle about single focus area)
- Task dependencies or blocking relationships (paused reason can reference but not enforce)
- Notifications (Constitution III prohibits notification spam; opt-in only, addressed in separate feature)
- Filtering/searching (addressed in separate feature; this feature focuses on core CRUD)
- Sync with external calendars or services
