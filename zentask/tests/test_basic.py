"""Basic tests for Zentask."""

import pytest
from datetime import datetime

from src.zentask.models.task import Task, TaskStatus
from src.zentask.services.task_service import TaskService
from src.zentask.services.audit_service import AuditService

def test_task_creation():
    """Test basic task creation."""
    service = TaskService()
    task = service.create("Test Task", "Test description")

    assert task.title == "Test Task"
    assert task.description == "Test description"
    assert task.status == TaskStatus.TO_DO
    assert task.id is not None

def test_task_status_change():
    """Test task status changes."""
    service = TaskService()
    task = service.create("Test Task")

    updated = service.change_status(task.id, TaskStatus.IN_PROGRESS)
    assert updated.status == TaskStatus.IN_PROGRESS

    updated = service.change_status(task.id, TaskStatus.DONE)
    assert updated.status == TaskStatus.DONE

def test_task_update():
    """Test task updates."""
    service = TaskService()
    task = service.create("Original Title")

    updated = service.update(task.id, title="Updated Title", description="New desc")
    assert updated.title == "Updated Title"
    assert updated.description == "New desc"

def test_task_deletion():
    """Test task deletion."""
    service = TaskService()
    task = service.create("Test Task")

    assert service.get(task.id) is not None
    result = service.delete(task.id)
    assert result is True
    assert service.get(task.id) is None

def test_invalid_task_creation():
    """Test validation on task creation."""
    service = TaskService()

    with pytest.raises(ValueError, match="title cannot be empty"):
        service.create("")

    with pytest.raises(ValueError, match="title cannot be empty"):
        service.create("   ")