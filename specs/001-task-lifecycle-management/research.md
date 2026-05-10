# Research & Analysis: Task Lifecycle Management

**Date**: 2026-05-09  
**Phase**: Phase 0 - Research & Clarification Resolution

## Technology Choices

### 1. Python 3.10+ as Primary Language

**Decision**: Python 3.10+ (matches system runtime, simple syntax)

**Rationale**:
- Streamlit requires Python; allows unified codebase (backend + frontend in same language)
- Rich ecosystem for data structures (dataclasses), testing (pytest), and utilities
- Single-user app doesn't require high performance; Python adequate

**Alternatives Considered**:
- Go/Rust: Overkill for single-user app; would require separate UI framework
- Node.js: Possible but Python + Streamlit is faster to prototype

**Decision Finalized**: ✅ Python 3.10+

---

### 2. Streamlit as Frontend Framework

**Decision**: Streamlit 1.28+

**Rationale**:
- Zero deployment friction (runs as web app locally)
- Reactive rendering built-in (auto-update on state change)
- Session state provides client-side optimism without explicit Redux-like patterns
- Limited keyboard support → address with external library (discussed below)

**Alternatives Considered**:
- PyQt/PySide: More control but requires GUI toolkit installation; steeper learning curve
- Django/Flask: Overkill for single-page app; more boilerplate
- Terminal UI (curses/rich): Text-only; harder to implement Constitution III (soft colors, generous typography)

**Decision Finalized**: ✅ Streamlit 1.28+

---

### 3. Keyboard Shortcut Implementation

**Decision**: Use `streamlit-shortcuts` library or custom JS injection for hotkey binding

**Rationale**:
- Constitution I requires `Ctrl+Shift+N`, `Ctrl+Q`, arrow navigation
- Streamlit native widgets lack global keyboard event capture
- External library (`streamlit-shortcuts`) or custom JS can intercept keypresses and trigger Streamlit callbacks

**Implementation Plan**:
- Install `streamlit-shortcuts` (or fork if unmaintained)
- Bind hotkeys in `ui/state.py` Streamlit session initialization
- Fallback: Custom HTML/JS component injected via `st.components.v1.html()`

**Alternatives Considered**:
- Selenium for testing only: Not viable for production UX
- Browser extensions: Out of scope; user friction

**Decision Finalized**: ✅ `streamlit-shortcuts` or custom JS hotkey layer

---

### 4. In-Memory State Management + JSON Lines Audit Log

**Decision**: 
- **State**: Python dict + dataclasses (no ORM)
- **Audit Trail**: JSON Lines (`.jsonl`) file in `data/audit.jsonl`

**Rationale**:
- Constitution IV mandates immutable event log; JSON Lines is append-only, human-readable, parseable
- No persistent task DB required (single-user, in-memory sufficient)
- Audit log file provides Constitutional compliance; user can export/delete history via UI
- Decouples state management from persistence

**Alternatives Considered**:
- SQLite: Adds complexity; JSON Lines simpler for audit trail use case
- Redis: Overkill for single-user, single-machine app
- Firestore/Cloud: Violates local-first storage principle

**Decision Finalized**: ✅ In-memory dict + JSON Lines audit log

---

### 5. MVC Architecture Pattern

**Decision**: Strict MVC separation:
- **Models** (`models/`): Pure dataclasses (Task, AuditEvent, Status enum)
- **Controllers/Services** (`services/`): Business logic (TaskService, AuditService)
- **Views** (`ui/`): Streamlit components and pages
- **Infrastructure** (`persistence/`): File I/O for audit log

**Rationale**:
- Constitution V mandates design patterns over hacks
- Testable: Services can be unit tested without Streamlit
- Reusable: Services layer can be swapped for different frontend later
- Maintainable: Clear separation of concerns

**Alternatives Considered**:
- Ad-hoc state management (directly mutating dict in Streamlit): Violates Constitution VI
- Single file monolith: Unmaintainable beyond 1000 LOC

**Decision Finalized**: ✅ MVC with clear layer separation

---

### 6. Testing Strategy

**Decision**:
- **Unit Tests**: pytest for models + services (no Streamlit)
- **Integration Tests**: Full workflow tests (create → status change → defer)
- **Test Data**: Factories in `tests/fixtures/`

**Rationale**:
- Services layer testable without UI; mock dataclasses
- Integration tests verify end-to-end workflows per feature spec
- Constitution V requires test-first development (TDD)

**Tools**:
- `pytest`: Standard Python testing framework
- `pytest-mock`: Mocking service dependencies
- `pytest-cov`: Coverage reports

**Decision Finalized**: ✅ pytest + fixtures for unit/integration testing

---

### 7. Mono-repo Structure

**Decision**: Single `zentask/` repository with `src/`, `tests/`, `docs/`

**Rationale**:
- Single-feature app; no reason for multiple repos
- Easier dependency management (single `requirements.txt`)
- Shared fixtures and utilities across test suite

**Alternatives Considered**:
- Separate backend/frontend repos: Unnecessary coupling for this app

**Decision Finalized**: ✅ Mono-repo structure

---

### 8. Configuration Management

**Decision**: 
- `src/zentask/config.py`: Constants (hotkey bindings, timeouts, paths)
- `.env.example`: Template for user-specific settings (log file path, theme, etc.)
- No secrets needed (single-user app)

**Rationale**:
- Constitution VI forbids hardcoded magic numbers
- Allows users to customize hotkeys per preferences file

**Decision Finalized**: ✅ Centralized config.py + .env template

---

## Constitution Alignment Verification

| Principle | Implementation |
|-----------|-----------------|
| **I. Keyboard-First** | `streamlit-shortcuts` + custom hotkey bindings in `ui/state.py` |
| **II. Instant Feedback** | Streamlit session state for optimistic updates; re-render on every action |
| **III. Anti-Anxiety** | Today's view filtering; paused task suppression; soft colors in theme |
| **IV. Audit Trail** | JSON Lines event log; immutable append-only; per service mutation |
| **V. Design Patterns** | MVC architecture; service layer for business logic; dataclasses for models |
| **VI. Anti-Patterns** | Constants in config.py; no silent failures; explicit error handling |

---

## Dependencies (Finalized)

### Core

```
streamlit==1.28.0
streamlit-shortcuts==0.1.0 (or equivalent hotkey library)
dataclasses-json==0.5.14 (for serializing Task/AuditEvent to JSON)
python-dateutil==2.8.2 (date parsing + timezone handling)
```

### Development/Testing

```
pytest==7.4.0
pytest-mock==3.11.1
pytest-cov==4.1.0
black==23.7.0 (code formatting)
flake8==6.0.0 (linting)
mypy==1.4.1 (type checking - optional but recommended)
```

### Optional (if needed)

```
python-dotenv==1.0.0 (for .env file loading)
rich==13.5.0 (better terminal output, logging)
```

---

## Open Questions Resolved

**Q**: How to handle missing hotkey library fallback?  
**A**: If `streamlit-shortcuts` unavailable, use HTML/JS injection. User can still access features via mouse; hotkeys are enhancement, not requirement.

**Q**: Should task data persist across app restarts?  
**A**: No. Per spec: "no persistent database, memory only". Audit log persists (user can export if needed).

**Q**: How to handle large task lists in memory?  
**A**: Python dict with task_id as key; O(1) lookup. 10k tasks → ~10MB memory (reasonable for single user).

---

## Next Steps (Phase 1: Design)

1. Create `data-model.md`: Task, AuditEvent, Status enum definitions
2. Create service contracts in `contracts/`: TaskService, AuditService interfaces
3. Create `quickstart.md`: Dev setup + running app locally
