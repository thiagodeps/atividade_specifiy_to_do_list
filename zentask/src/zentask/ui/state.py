"""Streamlit session state management for Zentask."""

import streamlit as st

from zentask.services import TaskService, AuditService

def get_task_service() -> TaskService:
    """Get or create task service in session state."""
    if "task_service" not in st.session_state:
        st.session_state.task_service = TaskService()
    return st.session_state.task_service

def get_audit_service() -> AuditService:
    """Get or create audit service in session state."""
    if "audit_service" not in st.session_state:
        st.session_state.audit_service = AuditService()
    return st.session_state.audit_service