#!/usr/bin/env python3
"""Run script for Zentask."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from zentask.ui import main

if __name__ == "__main__":
    main()