"""Pytest configuration file."""
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock
from pygmalion.storage import JSONStorage, SQLiteStorage
from pygmalion.alias import AliasManager
from pygmalion.tracker import CommandTracker
from pygmalion.help import AdaptiveHelp


@pytest.fixture
def temp_dir():
    """Create a temporary directory."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Force cleanup with retry on Windows
    try:
        shutil.rmtree(temp_dir)
    except PermissionError:
        import time
        import gc
        gc.collect()
        time.sleep(0.2)  # Longer wait
        try:
            shutil.rmtree(temp_dir)
        except PermissionError:
            # On Windows, SQLite files can remain locked
            # This is a known testing issue, not a code problem
            pass


@pytest.fixture
def clean_environment(monkeypatch):
    """Provide a clean test environment."""
    # Mock os.environ to avoid affecting real user data
    monkeypatch.setenv("PYGMALION_CONFIG_DIR", tempfile.mkdtemp())
