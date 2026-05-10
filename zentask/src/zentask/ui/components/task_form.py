"""Task form component for Zentask."""

import streamlit as st
from datetime import datetime

from zentask.services.task_service import TaskService

def show_task_form(task_service: TaskService, task_id: str = None):
    """Display a form for creating or editing a task."""
    task = task_service.get(task_id) if task_id else None

    with st.form(key=f"task_form_{task_id or 'new'}"):
        title = st.text_input(
            "Title *",
            value=task.title if task else "",
            max_chars=500,
            help="Task title (required)"
        )

        description = st.text_area(
            "Description",
            value=task.description or "" if task else "",
            max_chars=2000,
            height=100,
            help="Optional task description"
        )

        due_date = st.date_input(
            "Due Date",
            value=datetime.strptime(task.due_date, "%Y-%m-%d").date() if task and task.due_date else None,
            help="Optional due date"
        )

        submitted = st.form_submit_button("Save Task")

        if submitted:
            try:
                due_date_str = due_date.isoformat() if due_date else None

                if task_id:
                    # Update existing task
                    updated_task = task_service.update(
                        task_id=task_id,
                        title=title,
                        description=description,
                        due_date=due_date_str
                    )
                    st.success(f"Task '{updated_task.title}' updated!")
                else:
                    # Create new task
                    new_task = task_service.create(
                        title=title,
                        description=description,
                        due_date=due_date_str
                    )
                    st.success(f"Task '{new_task.title}' created!")

                st.rerun()

            except ValueError as e:
                st.error(f"Error: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")