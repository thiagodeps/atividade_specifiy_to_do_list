# Implementation Plan: Task Lifecycle Management

**Branch**: `001-task-lifecycle-management` | **Date**: 2026-05-09 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-task-lifecycle-management/spec.md`

**Note**: This plan is filled in by the `/speckit.plan` command. Architecture: Python backend + Streamlit frontend (MVC pattern in mono-repo).

## Summary

**Primary Requirement**: Implement core task lifecycle management (create, edit, delete, status transitions, defer, pause) with instant feedback (<100ms), audit trail for every mutation, and keyboard-first design.

**Technical Approach**: 
- **Backend (Model + Controller)**: Python service layer with in-memory state (dict/dataclasses) and immutable event log (JSON Lines)
- **Frontend (View)**: Streamlit for UI rendering with optimistic updates and keyboard hotkey bindings
- **Architecture**: MVC separation with business logic isolated from UI; state mutations trigger audit events
- **Storage**: In-memory Python objects + local JSON Lines audit log (no persistent database)
- **Testing**: Unit tests for service logic + integration tests for complete workflows

## Technical Context

**Language/Version**: Python 3.10+  
**Primary Dependencies**: Streamlit (UI framework), dataclasses (model definition), datetime (timestamp), json (audit log serialization)  
**Storage**: In-memory (Python dict/dataclasses) + JSON Lines audit log file (local disk for audit trail persistence per Constitution IV)  
**Testing**: pytest (unit tests), pytest-mock (mocking), custom fixtures for integration tests  
**Target Platform**: Local/desktop application (Streamlit web interface, runs on localhost)  
**Project Type**: Desktop/web application (single-user todo list)  
**Performance Goals**: Sub-100ms response for user actions (keyboard input → state update → UI render)  
**Constraints**: No persistent database; all task data in memory (lost on app restart unless exported); audit trail persisted locally as JSON Lines  
**Scale/Scope**: Single user; 1000s of tasks manageable in memory; < 5000 lines of core code

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

✅ **I. Keyboard-First Design**: Streamlit has limited native keyboard support; will implement custom hotkey layer using `streamlit_shortcuts` library or custom JS injection for `Ctrl+Shift+N`, `Ctrl+Q`, arrow navigation.  
✅ **II. Instant Feedback**: Streamlit re-renders on every widget interaction; optimistic updates via session state ensure sub-100ms perceived response.  
✅ **III. Anti-Anxiety Focus**: Today's view filtering implemented in view layer; paused tasks hidden via conditional rendering.  
✅ **IV. Trilha Auditoria**: Every service method that mutates state (create, update, delete, status_change, defer, pause) logs to immutable JSON Lines event log.  
✅ **V. Design Patterns**: MVC pattern enforced: Models (dataclasses) → Services (business logic) → Views (Streamlit UI); no mixed concerns.  
✅ **VI. Anti-Patterns Forbidden**: No hardcoded values (all constants in `config.py`); no silent failures (all exceptions logged); service methods are pure functions (state passed in, mutations logged).  

**Gate Status**: ✅ PASS - All principles alignable within Streamlit + Python architecture

## Project Structure

### Documentation (this feature)

```text
specs/001-task-lifecycle-management/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (Mono-repo, MVC Architecture)

```text
zentask/
├── README.md
├── requirements.txt
├── pyproject.toml
├── .env.example
│
├── src/
│   └── zentask/
│       ├── __init__.py
│       ├── config.py                 # Configuration + constants
│       ├── logger.py                 # Logging setup
│       │
│       ├── models/                   # M - Models (data structures)
│       │   ├── __init__.py
│       │   ├── task.py              # Task dataclass + enums (Status, Action)
│       │   └── audit_event.py       # AuditEvent dataclass
│       │
│       ├── services/                 # C - Controllers (business logic)
│       │   ├── __init__.py
│       │   ├── task_service.py      # Task CRUD + state transitions
│       │   └── audit_service.py     # Event logging + retrieval
│       │
│       ├── persistence/              # Infrastructure - audit log I/O
│       │   ├── __init__.py
│       │   └── json_log.py          # JSON Lines event log storage
│       │
│       └── ui/                       # V - View (Streamlit UI)
│           ├── __init__.py
│           ├── app.py               # Main Streamlit app entry point
│           ├── pages/
│           │   ├── __init__.py
│           │   ├── today.py         # Today's task view (P1)
│           │   ├── all_tasks.py     # All tasks view with filters
│           │   └── audit_log.py     # Audit trail viewer
│           ├── components/          # Reusable Streamlit components
│           │   ├── __init__.py
│           │   ├── task_form.py     # Task creation/edit form
│           │   ├── task_list.py     # Task list renderer
│           │   └── status_badge.py  # Status display component
│           └── state.py             # Streamlit session state management
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # pytest fixtures
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_task_model.py       # Model validation tests
│   │   ├── test_task_service.py     # Service logic tests
│   │   └── test_audit_service.py    # Audit logging tests
│   ├── integration/
│   │   ├── __init__.py
│   │   └── test_task_workflow.py    # End-to-end task workflows
│   └── fixtures/
│       ├── __init__.py
│       ├── sample_tasks.py          # Test data factories
│       └── mock_services.py         # Service mocks
│
└── docs/
    ├── ARCHITECTURE.md              # MVC pattern explanation
    ├── AUDIT_TRAIL.md              # Audit log format + retrieval
    └── KEYBOARD_SHORTCUTS.md       # Hotkey binding documentation
```

**Structure Decision**: Mono-repo with MVC separation:
- **Models** (`src/zentask/models/`): Pure dataclasses, no logic, framework-agnostic
- **Services** (`src/zentask/services/`): Business logic layer, state mutations, audit event creation
- **UI** (`src/zentask/ui/`): Streamlit views, handles input rendering and keyboard shortcuts
- **Persistence** (`src/zentask/persistence/`): Audit log file I/O (decoupled from models/services)
- **Tests** (`tests/`): Unit (models+services) and integration (full workflows) test coverage

## Complexity Tracking

**No Constitution violations** - MVC pattern and mono-repo structure are standard and well-established.

### Architectural Decisions

| Component | Decision | Rationale |
|-----------|----------|----------|
| State Management | Session state (Streamlit) + Service layer | Streamlit session persists across rerenders; service layer isolated for testing |
| Audit Log | JSON Lines file (`audit.jsonl`) | Immutable append-only format; human-readable; no DB dependency |
| Task Storage | In-memory dict (Python) | Single-user app; no persistence needed; O(1) lookup by task_id |
| UI Framework | Streamlit | Rapid prototyping, keyboard/mouse support, reactive rendering |
| Hotkey Binding | Custom Streamlit hook (JS injection or `streamlit-shortcuts` lib) | Native Streamlit limited; external lib needed for Constitution I compliance |
