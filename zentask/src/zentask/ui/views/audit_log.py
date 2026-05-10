"""Audit log page for Zentask."""

import streamlit as st
import pandas as pd

from zentask.services.audit_service import AuditService

def show_audit_log_page(audit_service: AuditService):
    """Display the audit log page."""
    st.title("📊 Audit Log")

    events = audit_service.get_all_events()

    if not events:
        st.info("No audit events yet.")
        return

    # Convert to DataFrame for display
    data = []
    for event in events:
        data.append({
            "Timestamp": event.timestamp,
            "User": event.user_id,
            "Action": event.action,
            "Task ID": event.task_id,
            "Details": str(event.details) if event.details else ""
        })

    df = pd.DataFrame(data)
    df = df.sort_values("Timestamp", ascending=False)

    st.dataframe(df, use_container_width=True)

    # Summary stats
    st.divider()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Events", len(events))

    with col2:
        actions = df["Action"].value_counts()
        most_common = actions.index[0] if not actions.empty else "None"
        st.metric("Most Common Action", most_common)

    with col3:
        unique_tasks = df["Task ID"].nunique()
        st.metric("Tasks with Events", unique_tasks)