"""Configuration constants for Zentask."""

import os
from pathlib import Path

# Application constants
APP_NAME = "Zentask"
APP_VERSION = "0.1.0"

# File paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
AUDIT_LOG_FILE = DATA_DIR / "audit_log.jsonl"

# Task constraints
MAX_TITLE_LENGTH = 500
MAX_DESCRIPTION_LENGTH = 2000

# UI constants
DEFAULT_PAGE_TITLE = "Zentask - Task Management"
DEFAULT_PAGE_ICON = "📋"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)