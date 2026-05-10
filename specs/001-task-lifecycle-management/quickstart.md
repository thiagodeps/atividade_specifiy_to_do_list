# Quick Start: Development Setup

**Date**: 2026-05-09  
**Phase**: Phase 1 - Quick Start Guide  

## Prerequisites

- Python 3.10+ installed
- pip or uv package manager
- Git (for version control)

## Installation & Setup

### 1. Clone Repository (or create project from template)

```bash
cd /home/thiagodeps/teste/meu-produto
mkdir zentask && cd zentask
```

### 2. Create Python Virtual Environment

```bash
# Using venv
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate

# Or using uv (faster)
uv venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
# Core dependencies
pip install -r requirements.txt

# Development dependencies (for testing/linting)
pip install -r requirements-dev.txt
```

### 4. Create Directory Structure

```bash
# From project root (zentask/)
mkdir -p src/zentask/{models,services,persistence,ui/{pages,components}}
mkdir -p tests/{unit,integration,fixtures}
mkdir -p docs data
```

### 5. Create Configuration Files

```bash
# Copy template files
cp .env.example .env
cp pyproject.toml.example pyproject.toml
```

### 6. Create Initial Files

Create `src/zentask/__init__.py` (empty or version string):
```python
__version__ = "0.1.0"
```

Create `src/zentask/config.py`:
```python
# Configuration constants (See data-model.md for structure)
TASK_TITLE_MAX_LENGTH = 500
TASK_DESCRIPTION_MAX_LENGTH = 2000
AUDIT_LOG_PATH = "data/audit.jsonl"
UNDO_WINDOW_SECONDS = 10
RESPONSE_TIME_TARGET_MS = 100

# Keyboard shortcuts
HOTKEYS = {
    "new_task": "ctrl+shift+n",
    "today_view": "ctrl+shift+d",
    "quick_search": "ctrl+q",
}

# Theme
THEME_COLORS = {
    "error": "#d4a574",  # Muted orange (not red)
    "success": "#90c890",
    "warning": "#d4a574",
}
```

## Running the Application

### Development Mode

```bash
# From project root
streamlit run src/zentask/ui/app.py
```

This will open `http://localhost:8501` in your browser.

### Production Mode (future)

```bash
streamlit run src/zentask/ui/app.py --logger.level=error
```

## Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/unit/test_task_service.py -v

# With coverage
pytest --cov=src/zentask tests/

# Watch mode (auto-run on file change, requires pytest-watch)
ptw
```

## Project Structure (Quick Reference)

```
zentask/
├── src/zentask/
│   ├── models/          # Data structures (Task, AuditEvent)
│   ├── services/        # Business logic (TaskService, AuditService)
│   ├── persistence/     # File I/O (JSON Lines audit log)
│   └── ui/              # Streamlit pages and components
├── tests/               # Unit + integration tests
├── docs/                # Architecture documentation
├── data/                # Runtime data (audit.jsonl)
├── requirements.txt     # Production dependencies
├── requirements-dev.txt # Dev/test dependencies
└── pyproject.toml       # Project metadata
```

## First Run Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Directory structure created
- [ ] Config files in place (`.env`, `pyproject.toml`)
- [ ] Run `streamlit run src/zentask/ui/app.py`
- [ ] Open `http://localhost:8501` in browser
- [ ] Create a test task and verify it appears in the list
- [ ] Run `pytest` to verify test framework works
- [ ] Check audit log file created at `data/audit.jsonl`

## Troubleshooting

### Streamlit not found
```bash
pip install streamlit==1.28.0
```

### Import errors (modules not found)
```bash
# Ensure PYTHONPATH includes src/
export PYTHONPATH="${PYTHONPATH}:${PWD}/src"
streamlit run src/zentask/ui/app.py
```

### Port 8501 already in use
```bash
streamlit run src/zentask/ui/app.py --server.port=8502
```

### Audit log file permissions
```bash
# Ensure data/ directory is writable
mkdir -p data
chmod 755 data
```

## Development Workflow

1. **Create feature branch**: `git checkout -b 001-task-create`
2. **Write tests first** (TDD per Constitution V):
   ```bash
   # Create test file: tests/unit/test_task_service.py
   # Write test_create_task() function
   pytest tests/unit/test_task_service.py::test_create_task -v
   ```
3. **Implement feature**: Fill in `src/zentask/services/task_service.py`
4. **Run tests**: `pytest` (ensure all pass)
5. **Test in Streamlit**: `streamlit run src/zentask/ui/app.py`
6. **Commit with principle reference**: `git commit -m "feat(I+IV): task creation with audit trail"`
7. **Push and create PR**

## Key Files to Implement (Phase 2)

| File | Purpose |
|------|---------|
| `models/task.py` | Task + TaskStatus dataclass definitions |
| `models/audit_event.py` | AuditEvent dataclass |
| `services/task_service.py` | TaskService class (CRUD + state transitions) |
| `services/audit_service.py` | AuditService class (event creation + logging) |
| `persistence/json_log.py` | JSON Lines audit log reader/writer |
| `ui/app.py` | Main Streamlit entry point |
| `ui/pages/today.py` | Today's task view |
| `ui/components/task_form.py` | Task creation/edit form |
| `tests/unit/test_task_service.py` | Service unit tests |
| `tests/integration/test_task_workflow.py` | End-to-end workflow tests |

## Next Steps

1. Clone this repo and follow setup above
2. Proceed to Phase 2 (`/speckit.tasks`) to generate detailed implementation tasks
3. Follow TDD workflow: test → implement → verify
4. Push commits with Constitution principle references
