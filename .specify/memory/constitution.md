# ZenTask Constitution
<!-- Todo list application: Keyboard-First, Instant Feedback, Anti-Anxiety Focus, Audit Trail -->

## Core Principles

### I. Keyboard-First Design
Every interaction MUST be accessible via keyboard without mouse dependency.
**Non-negotiable rules:**
- Global hotkeys registered: `Ctrl+Shift+N` (new task), `Ctrl+Shift+D` (today's focus), `Ctrl+Q` (quick search)
- Arrow keys navigate all lists; `Enter` selects; `Esc` cancels
- Tab/Shift+Tab never traps focus; modal dialogs always have escape hatch
- Keyboard hints visible in UI (e.g., `(K)` next to keybindable actions)
- User can remap hotkeys via preferences file without code recompile

**Rationale**: Reduces friction for power users and neurodivergent users who depend on keyboard workflows. Anxiety reduction through predictability and speed.

### II. Instant Feedback (Sub-100ms Response)
Every user action receives synchronous visual acknowledgment within 100ms.
**Non-negotiable rules:**
- Task creation: optimistic update (rendered immediately), server sync happens in background
- Task deletion: immediate removal from list + clear undo tooltip (`Undo - 10s`)
- Status toggles: update on-screen before any network call
- Loading states: spinner appears if operation exceeds 200ms (not before)
- Error feedback: non-blocking toasts (never alert dialogs); auto-dismiss after 5s unless user interacts
- Form submission: disabled button + loading spinner; prevent double-submit via race-condition guards

**Rationale**: Instant visual feedback reduces anxiety about whether an action registered. Prevents user frustration and excessive clicking.

### III. Anti-Anxiety Focus Architecture
Interface prioritizes calm, frictionless experience; removes unnecessary cognitive load.
**Non-negotiable rules:**
- Single focus area per screen (no overwhelming choice paralysis)
- Today's view shows ONLY tasks due today + overdue (no future clutter)
- Subtask expansion is opt-in (collapsed by default); prevents overwhelm from large task hierarchies
- No notification spam; opt-in notifications only (never auto-enable)
- Color palette: soft, desaturated colors (avoid red for errors if possible; use muted orange or amber)
- Typography: generous line-height (1.6x), font size ≥ 14px base for readability
- Confirmation dialogs only for destructive actions affecting >1 task or data loss
- One-click undo for destructive actions (deletion, archive, bulk ops)

**Rationale**: Reduces cortisol spikes from UI stress. Clear task scoping (today vs. later) helps executive dysfunction. Opt-in notifications prevent notification fatigue.

### IV. Trilha de Auditoria (Audit Trail - Non-Repudiation)
Every data mutation is logged with immutable, tamper-evident records.
**Non-negotiable rules:**
- All task mutations stored in immutable event log (JSON Lines format or similar)
- Event structure: `{timestamp_iso, user_id, action, task_id, before_state, after_state, reason}`
- Reason field captures why user made the change (e.g., "postponed due to blocked dependency")
- Local-first storage: events written to disk/device first, cloud sync is secondary
- Retention: audit logs kept indefinitely; user may export/delete entire history via privacy control
- No event deletion (soft-delete only); tombstone records mark removals
- Conflict resolution in sync: log shows all device edits; user chooses canonical version explicitly

**Rationale**: Trust and transparency. User can recover task history and explain to themselves (or others) why decisions were made. Supports regulatory/personal accountability.

### V. Design Patterns Over Hacks
All code follows established patterns; NO one-off solutions or shortcuts.
**Non-negotiable rules:**
- State management: use unidirectional data flow (Redux-like or MobX patterns, not ad-hoc mutations)
- Component structure: pure functions + hooks (or equivalent immutable model); no class mixins or God objects
- API contracts: versioned; deprecation warnings logged; no surprise breaking changes in minor releases
- Testing: unit tests for utils + state logic; integration tests for critical user workflows (e.g., task CRUD + sync)
- Error handling: explicit error types (not generic `Error`); handle all promises with `.catch()` or try/catch
- Documentation: README covers architecture; each module has JSDoc/docstring; non-obvious logic commented inline
- Secrets/config: never hardcoded; use environment variables or secure config file (not in repo)

**Rationale**: Prevents code rot and mysterious bugs. Makes onboarding and debugging faster. Reduces future re-work.

### VI. Anti-Patterns Explicitly Forbidden
The following MUST NOT appear in any feature branch or commit.
- **Silent failures**: Network errors that don't surface to logs or UI
- **Infinite loops / zombie processes**: setTimeout/setInterval without clear exit or useEffect cleanup
- **God components**: > 300 lines of JSX or logic in one file (split into smaller, composable units)
- **Magic numbers**: hardcoded timeouts, thresholds, or IDs; use named constants
- **Prop drilling**: passing data 5+ levels deep (use context or state management instead)
- **Temporal dead zones**: referencing variables before initialization; use const/let only
- **Mixed concerns**: UI component containing business logic (business logic in separate service/hook)
- **No input validation**: trusting user input or API responses; validate all boundaries
- **Callback hell**: Promises not used; deep nesting of callbacks (use async/await)
- **Inconsistent naming**: camelCase for JS, snake_case for DB; pick one per domain and stick to it
- **No rollback on bulk ops**: Bulk delete/update without atomic transactions or undo

## Developer Workflow

All features follow this sequence:
1. **Principle Check**: Does this feature align with one or more Core Principles? If not, propose an amendment first.
2. **Design Review**: Keyboard navigation map sketched; instant-feedback mechanism identified.
3. **TDD**: Test written first (happy path + edge cases); tests fail initially.
4. **Implementation**: Code written; anti-patterns checked via linter/reviewer.
5. **Integration Test**: Full user story tested end-to-end (keyboard + mouse, sync + offline).
6. **Audit Trail Verification**: Inspect logs; ensure events are immutable and complete.
7. **Accessibility Audit**: Screen reader test (if UI); keyboard-only user test.
8. **Merge**: All checks pass; PR description links to tests and architecture decision records (ADRs).



## Governance

This Constitution is the supreme law of ZenTask development. All code, issues, and PRs MUST comply.

**Amendment procedure:**
- Major change (new principle or removal): Open RFC issue, gather feedback for ≥ 1 week, vote by maintainers.
- Minor clarification or example addition: Fast-track if non-breaking (update version as PATCH).
- Conflict resolution: Use principle hierarchy: IV (Audit Trail) > III (Anti-Anxiety) > II (Instant Feedback) > I (Keyboard-First) > V (Patterns) >> VI (Anti-Patterns, absolute bars).

**Versioning**: Semantic versioning
- MAJOR: Principle removed or redefined incompatibly
- MINOR: New principle or substantial expansion of existing one
- PATCH: Wording, examples, clarifications

**Compliance review**: Every PR title must include principle reference, e.g. `feat(I+II): vim keybindings + 60ms response time`. Reviewer checks against constitution before approval.

**Version**: 1.0.0 | **Ratified**: 2026-05-09 | **Last Amended**: 2026-05-09
