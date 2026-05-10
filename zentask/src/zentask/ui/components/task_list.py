"""Task list component for Zentask."""

import streamlit as st

from zentask.services.task_service import TaskService
from zentask.models.task import Task, TaskStatus

def show_task_list(task_service: TaskService, tasks: list[Task], show_status_controls: bool = True):
    """Display a list of tasks with optional status controls."""
    for task in tasks:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.subheader(task.title)
                if task.description:
                    st.write(task.description)

                # Status badge
                status_colors = {
                    TaskStatus.TO_DO: "🔴",
                    TaskStatus.IN_PROGRESS: "🟡",
                    TaskStatus.DONE: "🟢",
                    TaskStatus.PAUSED: "⏸️"
                }
                st.write(f"{status_colors[task.status]} {task.status.value.replace('_', ' ').title()}")

                if task.due_date:
                    st.write(f"📅 Due: {task.due_date}")

                if task.pause_reason:
                    st.write(f"💭 {task.pause_reason}")

                st.caption(f"Created: {task.created_at[:10]}")

            with col2:
                if show_status_controls:
                    _show_status_controls(task_service, task)

            with col3:
                _show_action_buttons(task_service, task)

            st.divider()

def _show_status_controls(task_service: TaskService, task: Task):
    """Show status change controls for a task."""
    new_status = st.selectbox(
        "Status",
        [TaskStatus.TO_DO, TaskStatus.IN_PROGRESS, TaskStatus.DONE, TaskStatus.PAUSED],
        index=list(TaskStatus).index(task.status),
        format_func=lambda s: s.value.replace('_', ' ').title(),
        key=f"status_{task.id}"
    )

    if new_status != task.status:
        reason = None
        if new_status == TaskStatus.PAUSED:
            reason = st.text_input(
                "Pause reason",
                key=f"pause_reason_{task.id}",
                placeholder="Why is this task paused?"
            )

        if st.button("Update Status", key=f"update_status_{task.id}"):
            try:
                task_service.change_status(task.id, new_status, reason)
                st.success("Status updated!")
                st.rerun()
            except Exception as e:
                st.error(f"Error updating status: {e}")

def _show_action_buttons(task_service: TaskService, task: Task):
    """Show action buttons for a task."""
    col1, col2 = st.columns(2)

    with col1:
        if st.button("✏️ Edit", key=f"edit_{task.id}"):
            st.session_state[f"editing_{task.id}"] = True

    with col2:
        if st.button("🗑️ Delete", key=f"delete_{task.id}"):
            if st.session_state.get(f"confirm_delete_{task.id}", False):
                try:
                    task_service.delete(task.id)
                    st.success("Task deleted!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting task: {e}")
            else:
                st.session_state[f"confirm_delete_{task.id}"] = True
                st.warning("Click again to confirm deletion")

    # Show edit form if editing
    if st.session_state.get(f"editing_{task.id}", False):
        with st.expander("Edit Task", expanded=True):
            from zentask.ui.components.task_form import show_task_form
            show_task_form(task_service, task.id)

            if st.button("Cancel Edit", key=f"cancel_edit_{task.id}"):
                st.session_state[f"editing_{task.id}"] = False
                st.rerun()