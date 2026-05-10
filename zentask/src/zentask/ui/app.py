"""Main Streamlit application for Zentask."""

import streamlit as st

from zentask.config import DEFAULT_PAGE_TITLE, DEFAULT_PAGE_ICON
from zentask.services import TaskService, AuditService
from zentask.ui.views.today import show_today_page
from zentask.ui.views.all_tasks import show_all_tasks_page
from zentask.ui.views.audit_log import show_audit_log_page
from zentask.ui.state import get_task_service, get_audit_service

def main():
    """Main application entry point."""
    st.set_page_config(
        page_title=DEFAULT_PAGE_TITLE,
        page_icon=DEFAULT_PAGE_ICON,
        layout="wide"
    )

    # Initialize services in session state
    task_service = get_task_service()
    audit_service = get_audit_service()

    # Sidebar navigation
    st.sidebar.title("📋 Zentask")
    page = st.sidebar.radio(
        "Navigation",
        ["Today", "All Tasks", "Audit Log"],
        key="nav"
    )

    # Main content
    if page == "Today":
        show_today_page(task_service)
    elif page == "All Tasks":
        show_all_tasks_page(task_service)
    elif page == "Audit Log":
        show_audit_log_page(audit_service)

if __name__ == "__main__":
    main()