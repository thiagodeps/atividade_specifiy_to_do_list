# Tasks: Task Lifecycle Management

**Input**: Design documents from `/specs/001-task-lifecycle-management/`  
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/  
**Target Platform**: Python 3.10+ with Streamlit 1.28+  
**Architecture**: MVC (mono-repo) with in-memory state + JSON Lines audit log  

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label (US1, US2, US3, etc.)
- File paths relative to project root

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Initialize Python project structure and dependencies

- [ ] T001 Create project root structure: `mkdir -p zentask/{src/zentask/{models,services,persistence,ui/{pages,components}},tests/{unit,integration,fixtures},docs,data}`
- [ ] T002 Create `zentask/requirements.txt` with core dependencies: streamlit==1.28.0, dataclasses-json==0.5.14, python-dateutil==2.8.2
- [ ] T003 Create `zentask/requirements-dev.txt` with pytest==7.4.0, pytest-mock==3.11.1, pytest-cov==4.1.0, black==23.7.0, flake8==6.0.0
- [ ] T004 Create `zentask/pyproject.toml` with project metadata, version 0.1.0, python_requires>=3.10
- [ ] T005 Create `zentask/.env.example` with `AUDIT_LOG_PATH=data/audit.jsonl`, `HOTKEY_NEW_TASK=ctrl+shift+n`
- [ ] T006 [P] Create `zentask/.gitignore` ignoring .venv/, __pycache__/, *.pyc, .env, data/audit.jsonl
- [ ] T007 [P] Create `zentask/README.md` with project description, quick start, and architecture overview
- [ ] T008 [P] Initialize Git repo: `git init && git add . && git commit -m "init: project structure"`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure for all user stories; MUST complete before story implementation begins

### Models & Enums Base

- [ ] T009 Create `src/zentask/models/__init__.py` (empty or import exports)
- [ ] T010 Create `src/zentask/models/task.py` with Task dataclass (id, title, description, status, due_date, created_at, updated_at, pause_reason) and validation in `__post_init__` per data-model.md
- [ ] T011 Create TaskStatus enum in `src/zentask/models/task.py` with values: TO_DO, IN_PROGRESS, DONE, PAUSED
- [ ] T012 [P] Create `src/zentask/models/audit_event.py` with AuditEvent frozen dataclass (timestamp, user_id, action, task_id, before_state, after_state, reason) per data-model.md
- [ ] T013 [P] Create Action enum in `src/zentask/models/audit_event.py` with values: CREATE, UPDATE, DELETE, STATUS_CHANGE, DEFER, PAUSE

### Configuration & Logging

- [ ] T014 Create `src/zentask/config.py` with constants: TASK_TITLE_MAX=500, TASK_DESC_MAX=2000, AUDIT_LOG_PATH="data/audit.jsonl", UNDO_WINDOW_SECONDS=10, RESPONSE_TARGET_MS=100
- [ ] T015 [P] Create hotkey constants in `src/zentask/config.py`: NEW_TASK="ctrl+shift+n", TODAY_VIEW="ctrl+shift+d", QUICK_SEARCH="ctrl+q"
- [ ] T016 [P] Create theme constants in `src/zentask/config.py`: error_color="#d4a574", success_color="#90c890", warning_color="#d4a574"
- [ ] T017 Create `src/zentask/logger.py` with setup_logger() function using Python logging with file/console handlers

### Persistence Infrastructure

- [ ] T018 Create `src/zentask/persistence/__init__.py` (empty or imports)
- [ ] T019 Create `src/zentask/persistence/json_log.py` with JsonEventLog class: append_event(event: AuditEvent), read_events() -> List[AuditEvent], clear_log() methods per contracts/services.md
- [ ] T020 [P] Implement event serialization (dataclass to dict/JSON) in `src/zentask/persistence/json_log.py` using dataclasses.asdict()

### Core Package Setup

- [ ] T021 Create `src/zentask/__init__.py` with `__version__ = "0.1.0"`
- [ ] T022 [P] Create `tests/__init__.py` (empty)
- [ ] T023 [P] Create `tests/conftest.py` with pytest fixtures for sample tasks, services, and audit log setup

**⚠️ CRITICAL CHECKPOINT**: Foundation complete - User Story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create a New Task (Priority: P1) 🎯 MVP

**Goal**: Users can register new tasks with title, optional description, and due date

**Independent Test**: Create a task → verify it appears in task list with TO_DO status → verify audit log entry created

### Tests for US1 (Write FIRST, ensure FAIL before implementation)

- [ ] T024 [P] [US1] Unit test `tests/unit/test_task_model.py::test_task_creation_valid` - create Task with title, verify id generated, status=TO_DO, timestamps set
- [ ] T025 [P] [US1] Unit test `tests/unit/test_task_model.py::test_task_creation_empty_title` - create Task with empty title raises ValueError
- [ ] T026 [US1] Integration test `tests/integration/test_task_workflow.py::test_create_task_workflow` - create task, verify in list, verify audit log entry with action=CREATE

### Implementation for US1

- [ ] T027 [US1] Create `src/zentask/services/__init__.py` (empty or imports)
- [ ] T028 [US1] Create `src/zentask/services/audit_service.py` with AuditService class: log_event(), get_events(), export_audit_log(), clear_audit_log() per contracts/services.md
- [ ] T029 [US1] Create `src/zentask/services/task_service.py` with TaskService class skeleton (in-memory dict store, next_task_id counter)
- [ ] T030 [US1] Implement TaskService.create(title, description=None, due_date=None) → Task method in `src/zentask/services/task_service.py` per contracts/services.md
- [ ] T031 [US1] Implement TaskService.list() method returning all tasks from in-memory store
- [ ] T032 [US1] Update TaskService.create() to log AuditEvent with action=CREATE via AuditService.log_event()
- [ ] T033 [P] [US1] Create Streamlit UI skeleton `src/zentask/ui/__init__.py` (empty)
- [ ] T034 [P] [US1] Create `src/zentask/ui/state.py` with Streamlit session state initialization for tasks dict and audit service instance
- [ ] T035 [P] [US1] Create `src/zentask/ui/components/__init__.py` and `src/zentask/ui/components/task_form.py` with task creation form component (title input, description textarea, due_date input)
- [ ] T036 [P] [US1] Create `src/zentask/ui/components/task_list.py` with task list rendering component (columns: title, status badge, due date, actions)
- [ ] T037 [US1] Create `src/zentask/ui/pages/__init__.py` and `src/zentask/ui/pages/today.py` main page with task creation form + today's task list
- [ ] T038 [US1] Create `src/zentask/ui/app.py` Streamlit main entry point: load state, show today page, handle keyboard shortcuts
- [ ] T039 [US1] Implement optimistic UI update in task_form.py: show task immediately on list before audit log write completes
- [ ] T040 [US1] Add error handling and validation feedback for empty title (show error toast)
- [ ] T041 [US1] Test full flow: `streamlit run src/zentask/ui/app.py` → create task → verify in list → check `data/audit.jsonl` contains CREATE event

**Checkpoint**: User Story 1 complete - users can create tasks with instant feedback and audit trail

---

## Phase 4: User Story 2 - Update Task Status (Priority: P1)

**Goal**: Users can mark tasks as In Progress or Done with single-click/keyboard action

**Independent Test**: Create task → mark as In Progress → verify status change on screen within 100ms → verify Done transition works → verify revert to To Do works

### Tests for US2

- [ ] T042 [P] [US2] Unit test `tests/unit/test_task_service.py::test_change_status_valid` - call change_status(TO_DO→IN_PROGRESS) verifies status updates
- [ ] T043 [P] [US2] Unit test `tests/unit/test_task_service.py::test_status_transitions_reversible` - test all valid transitions (To Do ↔ In Progress ↔ Done, all ↔ Paused)
- [ ] T044 [US2] Integration test `tests/integration/test_task_workflow.py::test_status_change_workflow` - full workflow create → change status 3x → verify audit log has 3 STATUS_CHANGE events

### Implementation for US2

- [ ] T045 [US2] Implement TaskService.change_status(task_id, new_status, reason=None) method in `src/zentask/services/task_service.py` per contracts/services.md
- [ ] T046 [US2] Add state machine validation in change_status() (all transitions allowed per feature spec)
- [ ] T047 [US2] Update change_status() to log AuditEvent with action=STATUS_CHANGE including before/after states
- [ ] T048 [P] [US2] Create `src/zentask/ui/components/status_badge.py` with status display (TO_DO, IN_PROGRESS, DONE, PAUSED colored badges)
- [ ] T049 [P] [US2] Add status toggle buttons to task_list.py for quick status transitions (cycle To Do → In Progress → Done → To Do)
- [ ] T050 [US2] Implement keyboard navigation in task_list.py (arrow keys select task, Enter toggles status, Esc deselect)
- [ ] T051 [US2] Connect status buttons to TaskService.change_status() with optimistic UI update
- [ ] T052 [US2] Add 100ms response time validation: measure time from button click to UI update
- [ ] T053 [US2] Test full flow: create task → cycle status with buttons/keyboard → verify audit log events

**Checkpoint**: User Story 2 complete - status tracking works with instant feedback and keyboard support

---

## Phase 5: User Story 3 - Edit Task Details (Priority: P1)

**Goal**: Users can modify task title, description, and due date after creation

**Independent Test**: Create task → edit title → edit description → edit due date → verify all changes persist → verify audit log shows EDIT events with old/new values

### Tests for US3

- [ ] T054 [P] [US3] Unit test `tests/unit/test_task_service.py::test_update_task` - call update(title, description, due_date) verifies all fields update
- [ ] T055 [P] [US3] Unit test `tests/unit/test_task_service.py::test_update_task_empty_title_fails` - update with empty title raises ValueError
- [ ] T056 [US3] Integration test `tests/integration/test_task_workflow.py::test_edit_task_workflow` - create → edit multiple fields → verify audit log shows UPDATE with before/after states

### Implementation for US3

- [ ] T057 [US3] Implement TaskService.update(task_id, title=None, description=None, due_date=None) method in `src/zentask/services/task_service.py` per contracts/services.md
- [ ] T058 [US3] Add title/date validation in update() method (non-empty title, valid ISO 8601 date)
- [ ] T059 [US3] Update update() to log AuditEvent with action=UPDATE including before/after states
- [ ] T060 [P] [US3] Create `src/zentask/ui/components/task_detail_modal.py` with task edit form (title, description, due_date fields, save/cancel buttons)
- [ ] T061 [P] [US3] Update task_list.py to show "Edit" button/action on each task row
- [ ] T062 [US3] Connect edit button to task_detail_modal.py, populate form with current task data
- [ ] T063 [US3] Connect save button to TaskService.update() with optimistic UI update
- [ ] T064 [US3] Add edit mode to task rows: click to open modal, make changes, verify fields update in-place with updated_at timestamp
- [ ] T065 [US3] Test full flow: create task → edit title → edit description → edit due_date → verify all changes in audit log

**Checkpoint**: User Story 3 complete - all task fields editable with audit trail

---

## Phase 6: User Story 4 - Delete or Archive Tasks (Priority: P2)

**Goal**: Users can remove tasks from active list with undo capability and permanent deletion support

**Independent Test**: Create task → delete → task disappears from list → undo within 10s → task reappears → verify audit log shows DELETE → wait 10s → permanent deletion

### Tests for US4

- [ ] T066 [P] [US4] Unit test `tests/unit/test_task_service.py::test_delete_task` - call delete(task_id) verifies removed from list, returns True
- [ ] T067 [P] [US4] Unit test `tests/unit/test_task_service.py::test_undo_delete` - call delete then undo_delete restores task
- [ ] T068 [US4] Integration test `tests/integration/test_task_workflow.py::test_delete_undo_workflow` - delete task, verify undo message shows, verify undo restores, verify audit log has DELETE then CREATE (restoration)

### Implementation for US4

- [ ] T069 [US4] Implement TaskService.delete(task_id) → bool method in `src/zentask/services/task_service.py` per contracts/services.md (removes from dict, logs DELETE event)
- [ ] T070 [US4] Implement TaskService.undo_delete(task_id, previous_state) → Task method in `src/zentask/services/task_service.py` (re-adds to dict)
- [ ] T071 [US4] Update delete() to store task state (for undo window) and log AuditEvent with action=DELETE
- [ ] T072 [P] [US4] Create `src/zentask/ui/components/undo_toast.py` with 10-second countdown timer display
- [ ] T073 [P] [US4] Add delete button to task_list.py (trash icon or action menu)
- [ ] T074 [US4] Connect delete button to TaskService.delete() with optimistic removal from UI
- [ ] T075 [US4] Show undo_toast.py after deletion with 10s countdown
- [ ] T076 [US4] Implement undo button to call TaskService.undo_delete() within 10-second window
- [ ] T077 [US4] After 10-second timeout, mark task as permanently deleted (no undo possible)
- [ ] T078 [US4] Test full flow: create task → delete → verify disappears → undo within 10s → verify reappears → verify audit log

**Checkpoint**: User Story 4 complete - task deletion with undo support

---

## Phase 7: User Story 5 - Defer / Postpone Tasks (Priority: P2)

**Goal**: Users can move tasks to future dates, hiding them from today's view

**Independent Test**: Create task due today → defer to next week → task disappears from today's view → navigate to that week → task appears with new due date → verify audit log shows DEFER event

### Tests for US5

- [ ] T079 [P] [US5] Unit test `tests/unit/test_task_service.py::test_defer_task` - call defer(task_id, new_date) updates due_date, returns updated Task
- [ ] T080 [P] [US5] Unit test `tests/unit/test_task_service.py::test_defer_task_invalid_date` - defer with invalid date format raises ValueError
- [ ] T081 [US5] Integration test `tests/integration/test_task_workflow.py::test_defer_workflow` - create task today → defer to future → verify disappears from today view → verify in future view → verify audit log

### Implementation for US5

- [ ] T082 [US5] Implement TaskService.defer(task_id, new_due_date) → Task method in `src/zentask/services/task_service.py` per contracts/services.md
- [ ] T083 [US5] Add date validation in defer() (must be ISO 8601 YYYY-MM-DD format)
- [ ] T084 [US5] Update defer() to log AuditEvent with action=DEFER including before/after due dates
- [ ] T085 [US5] Implement today's task view filter in today.py: show only tasks where due_date == today OR due_date < today (overdue)
- [ ] T086 [P] [US5] Create `src/zentask/ui/pages/all_tasks.py` with all tasks view (no date filter, show all tasks + status)
- [ ] T087 [P] [US5] Add date picker button/modal for defer action in task_list.py
- [ ] T088 [US5] Connect defer action to TaskService.defer(task_id, new_date) with calendar picker
- [ ] T089 [US5] Update today.py filter to exclude deferred tasks (due_date > today)
- [ ] T090 [US5] Test full flow: create task due today → defer 1 week → verify gone from today view → verify in all_tasks view

**Checkpoint**: User Story 5 complete - task deferral with today's focus

---

## Phase 8: User Story 6 - Pause / Mark as Indeterminate (Priority: P2)

**Goal**: Users can mark tasks as Paused (blocked/waiting) to suppress from active work without deletion

**Independent Test**: Create task, mark In Progress → pause with reason → task hidden from active list → unpause → task reappears in active list → verify audit log shows PAUSE/UNPAUSE

### Tests for US6

- [ ] T091 [P] [US6] Unit test `tests/unit/test_task_service.py::test_pause_task` - call change_status(PAUSED, reason="...") updates status and pause_reason
- [ ] T092 [P] [US6] Unit test `tests/unit/test_task_service.py::test_pause_reason_optional` - pause can be called with or without reason
- [ ] T093 [US6] Integration test `tests/integration/test_task_workflow.py::test_pause_unpause_workflow` - create → mark in_progress → pause with reason → verify hidden → unpause → verify reappears

### Implementation for US6

- [ ] T094 [US6] Update TaskService.change_status() to handle PAUSED status and optional pause_reason field in `src/zentask/services/task_service.py`
- [ ] T095 [US6] When status=PAUSED, populate task.pause_reason from reason parameter; log action=PAUSE instead of STATUS_CHANGE
- [ ] T096 [US6] Update TaskService.list() to accept status_filter parameter for filtering by status
- [ ] T097 [P] [US6] Create `src/zentask/ui/components/pause_reason_modal.py` with reason input field and save button
- [ ] T098 [P] [US6] Add "Pause" button to task actions in task_list.py
- [ ] T099 [US6] Connect pause action to pause_reason_modal.py, then TaskService.change_status(PAUSED, reason)
- [ ] T100 [US6] Update today.py filter: exclude PAUSED tasks from today's active view
- [ ] T101 [US6] Create optional "Paused Tasks" section in today.py showing paused tasks separately (collapsed/hidden by default)
- [ ] T102 [US6] Implement unpause: click paused task → option to resume (change_status back to original status like IN_PROGRESS)
- [ ] T103 [US6] Test full flow: create → in progress → pause with reason → verify hidden from today → unpause → verify reappears

**Checkpoint**: User Story 6 complete - task pause/block functionality

---

## Phase 9: Audit Trail Viewer & Export

**Goal**: Users can view complete task history and export audit trail

### Tests for Audit

- [ ] T104 [P] Audit export test `tests/integration/test_audit.py::test_audit_export_format` - export audit log, verify JSON Lines format with all events
- [ ] T105 [P] Audit retrieval test `tests/integration/test_audit.py::test_get_task_history` - get events for specific task, verify chronological order

### Implementation for Audit

- [ ] T106 Create `src/zentask/ui/pages/audit_log.py` audit trail viewer page
- [ ] T107 [P] Implement audit log display with filters: by task_id, by action type, date range picker
- [ ] T108 [P] Add export button to audit_log.py: calls AuditService.export_audit_log(), downloads as audit.jsonl
- [ ] T109 Add "Clear Audit Log" button with confirmation modal: calls AuditService.clear_audit_log() (privacy control per Constitution IV)
- [ ] T110 Add audit_log.py link to main navigation menu in app.py

---

## Phase 10: Keyboard Shortcuts & Hotkey Integration

**Goal**: Complete keyboard-first design per Constitution I with global hotkeys

### Implementation for Hotkeys

- [ ] T111 Install `streamlit-shortcuts` library in requirements.txt (or implement custom JS hotkey binding)
- [ ] T112 [P] Create hotkey bindings in state.py: Ctrl+Shift+N (new task), Ctrl+Shift+D (today view), Ctrl+Q (quick search)
- [ ] T113 [P] Implement arrow key navigation in task_list.py (select task up/down, change status with Ctrl+, defer with Ctrl+D)
- [ ] T114 Add keyboard help modal (?) showing all available shortcuts
- [ ] T115 Test all hotkeys: Ctrl+Shift+N opens new task form, Ctrl+Shift+D navigates to today, etc.

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Final refinement, testing, and documentation

### Testing & Coverage

- [ ] T116 [P] Run `pytest tests/ --cov=src/zentask` verify >= 80% code coverage
- [ ] T117 [P] Add unit test `tests/unit/test_json_log.py` for persistence layer (append, read, clear operations)
- [ ] T118 [P] Add unit test `tests/unit/test_config.py` for configuration constants loading
- [ ] T119 Run full integration test suite: `pytest tests/integration/` ensure all workflows pass
- [ ] T120 Manual end-to-end test: follow quickstart.md steps, verify all 6 user stories work

### Documentation & Code Quality

- [ ] T121 [P] Update `zentask/docs/ARCHITECTURE.md` with MVC pattern explanation, service contracts, data flow diagram
- [ ] T122 [P] Update `zentask/docs/AUDIT_TRAIL.md` with JSON Lines format specification, event types, retrieval examples
- [ ] T123 [P] Create `zentask/docs/KEYBOARD_SHORTCUTS.md` with all hotkey bindings and navigation patterns
- [ ] T124 Format code with black: `black src/ tests/`
- [ ] T125 Lint code with flake8: `flake8 src/ tests/` fix any violations
- [ ] T126 Add docstrings to all public methods (TaskService, AuditService, UI components)
- [ ] T127 [P] Add inline comments for non-obvious logic in services layer

### Validation & Deployment Readiness

- [ ] T128 Verify `data/` directory creation and audit log file persistence across app restarts
- [ ] T129 Test concurrent task creation: create multiple tasks in rapid succession, verify no race conditions in audit log
- [ ] T130 Verify optimistic UI updates: measure response time for all actions, confirm < 100ms perception (T052 repeat)
- [ ] T131 Test error scenarios: invalid due dates, network failures (if applicable), file permission errors
- [ ] T132 Validate Constitution alignment checklist per GEMINI.md principles I-VI
- [ ] T133 Final commit with message: `feat: complete task lifecycle management (create, edit, delete, defer, pause, audit)`

---

## Dependencies & Execution Order

### Critical Path (Sequential - Blocking)

1. **Phase 1 (Setup)**: T001-T008 - Project structure (must complete first)
2. **Phase 2 (Foundational)**: T009-T023 - Models, config, persistence (blocks all stories)
3. Then: **Phases 3-8 (User Stories)** can run in parallel **OR** sequentially P1 → P2 → P3

### Parallel Opportunities

**After Phase 2 completes**:
- All 6 user stories (Phases 3-8) can be implemented in parallel by different developers
- Within each phase:
  - All [P] marked tests can run in parallel
  - Multiple [P] marked implementation tasks can run in parallel (different files)
  - Tests for a story marked [P] should complete before implementation starts

**Phases 9-11 (Audit + Polish)** depend on most/all user stories; can start after Phase 8 implementation tasks complete

### Sequential Within Story (Enforced)

1. Write tests (if included) - ensure FAIL
2. Implement models
3. Implement services
4. Implement UI components
5. Integration testing
6. Move to next story

---

## Parallel Execution Example

**Scenario**: 3 developers, want to complete MVP (Phases 3-5) in parallel

```bash
# Developer 1: User Story 1 (Create Task)
Phase 3: T024-T041 (tests + implementation)

# Developer 2: User Story 2 (Update Status) - can start after Phase 2
Phase 4: T042-T053 (tests + implementation)
  Dependency: TaskService from Phase 3 (T029)
  Waits for T029 (TaskService skeleton), then develops in parallel

# Developer 3: User Story 3 (Edit Task) - can start after Phase 2
Phase 5: T054-T065 (tests + implementation)
  Dependency: TaskService from Phase 3 (T030)
  Waits for T030 (create method), then develops in parallel

# All merge to main when individual phases complete with tests green
```

---

## Suggested MVP Scope

**Minimum Viable Product** (Phases 1-5):

- [ ] Users can **create** tasks (US1)
- [ ] Users can **mark status** as In Progress / Done (US2)
- [ ] Users can **edit** task details (US3)
- Includes: instant feedback, audit trail, keyboard support for all actions
- Excludes: delete, defer, pause (P2 stories - nice-to-have)

**MVP Tasks**: T001-T065 (approximately 65 tasks)  
**MVP Time**: ~5-7 days for 1 developer (TDD + testing)  
**Post-MVP Addition**: Phases 6-8 (delete, defer, pause) adds ~40 tasks

---

## Task Status Legend

- **P1 Priority**: 3 core user stories (Create, Status, Edit) - MVP
- **P2 Priority**: 3 advanced stories (Delete, Defer, Pause) - post-MVP
- **[P] Marker**: 74 tasks can run in parallel; sequential dependencies marked in task descriptions
- **[Story] Label**: Phase/story context (US1-US6); helps organize by feature
- **File Paths**: All paths relative to `zentask/` project root

---

## Getting Started

```bash
# Step 1: Complete Phase 1
cd zentask && python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Step 2: Complete Phase 2 (run tests for each task)
pytest tests/unit/test_task_model.py -v
pytest tests/unit/test_task_service.py -v

# Step 3: Run Phase 3 User Story 1
# Write tests first (T024-T026), ensure FAIL
pytest tests/unit/test_task_model.py::test_task_creation_valid -v
# Should FAIL before T027 is started
# Then implement T027-T041

# Step 4: Run Streamlit app
streamlit run src/zentask/ui/app.py

# Step 5: Iterate through remaining user stories
```

---

## Next Steps

1. **Start Phase 1**: Run setup tasks T001-T008
2. **Run Phase 2**: Implement foundational models/services T009-T023
3. **Choose MVP or Full**: 
   - MVP: Focus Phases 3-5 (P1 stories) only
   - Full: Complete all Phases 3-8 (P1+P2 stories)
4. **Execute in parallel or sequential**: Use task dependencies above
5. **Final validation**: Complete Phases 9-11 (Audit, Hotkeys, Polish)
