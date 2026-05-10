"""All tasks page for Zentask."""

import streamlit as st

from zentask.services.task_service import TaskService
from zentask.models.task import TaskStatus
from zentask.ui.components.task_form import show_task_form
from zentask.ui.components.task_list import show_task_list

def show_all_tasks_page(task_service: TaskService):
    """Display all tasks page with filtering."""
    st.title("📋 All Tasks")

    # Filters
    col1, col2 = st.columns([2, 1])

    with col1:
        status_filter = st.selectbox(
            "Filter by status",
            ["All", "To Do", "In Progress", "Done", "Paused"],
            key="status_filter"
        )

    with col2:
        show_form = st.checkbox("Show add task form", value=False, key="show_form")

    if show_form:
        with st.expander("➕ Add New Task", expanded=True):
            show_task_form(task_service)
        st.divider()

    # Convert filter to enum
    status_map = {
        "To Do": TaskStatus.TO_DO,
        "In Progress": TaskStatus.IN_PROGRESS,
        "Done": TaskStatus.DONE,
        "Paused": TaskStatus.PAUSED,
    }

    if status_filter == "All":
        tasks = task_service.list()
    else:
        tasks = task_service.list(status_map[status_filter])

    if tasks:
        st.subheader(f"Tasks ({len(tasks)})")
        show_task_list(task_service, tasks, show_status_controls=True)
    else:
        st.info("No tasks found with the selected filter.")