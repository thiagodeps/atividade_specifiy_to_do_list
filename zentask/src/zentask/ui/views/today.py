"""Today page for Zentask - shows active tasks."""

import streamlit as st
from datetime import datetime, timezone

from zentask.services.task_service import TaskService
from zentask.models.task import TaskStatus
from zentask.ui.components.task_form import show_task_form
from zentask.ui.components.task_list import show_task_list

def show_today_page(task_service: TaskService):
    """Display the today page with active tasks."""
    st.title("📅 Today")

    # Quick add task
    with st.expander("➕ Add New Task", expanded=False):
        show_task_form(task_service)

    st.divider()

    # Active tasks (not done)
    active_tasks = [
        task for task in task_service.list()
        if task.status in [TaskStatus.TO_DO, TaskStatus.IN_PROGRESS, TaskStatus.PAUSED]
    ]

    if active_tasks:
        st.subheader(f"Active Tasks ({len(active_tasks)})")
        show_task_list(task_service, active_tasks, show_status_controls=True)
    else:
        st.info("No active tasks. Add one above to get started!")

    # Today's completed tasks
    today = datetime.now(timezone.utc).date().isoformat()
    completed_today = [
        task for task in task_service.list(TaskStatus.DONE)
        if task.updated_at.startswith(today)
    ]

    if completed_today:
        st.divider()
        st.subheader(f"✅ Completed Today ({len(completed_today)})")
        show_task_list(task_service, completed_today, show_status_controls=False)