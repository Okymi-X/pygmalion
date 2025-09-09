"""
Test configuration and fixtures for Pygmalion test suite.
"""

import pytest
import tempfile
import os
from pathlib import Path


@pytest.fixture(scope="session")
def test_data_dir():
    """Create a temporary directory for test data."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture(scope="function") 
def clean_environment(monkeypatch):
    """Ensure clean environment for each test."""
    # Remove any existing Pygmalion environment variables
    env_vars_to_remove = [
        "PYGMALION_STORAGE_PATH",
        "PYGMALION_CONFIG_PATH",
        "PYGMALION_DEBUG"
    ]
    
    for var in env_vars_to_remove:
        monkeypatch.delenv(var, raising=False)


@pytest.fixture
def sample_command_history():
    """Sample command history data for testing."""
    from datetime import datetime, timedelta
    
    base_time = datetime.now()
    
    return [
        {
            "command": "export",
            "args": {"format": "json", "verbose": True},
            "timestamp": (base_time - timedelta(hours=1)).isoformat()
        },
        {
            "command": "process", 
            "args": {"backup": True},
            "timestamp": (base_time - timedelta(minutes=30)).isoformat()
        },
        {
            "command": "export",
            "args": {"format": "csv"},
            "timestamp": (base_time - timedelta(minutes=10)).isoformat()
        },
        {
            "command": "scan",
            "args": {"recursive": True, "verbose": True},
            "timestamp": base_time.isoformat()
        }
    ]


@pytest.fixture
def sample_aliases():
    """Sample aliases data for testing."""
    return {
        "export-json": {
            "command": "export",
            "args": {"format": "json", "verbose": True},
            "description": "Quick JSON export",
            "created": "2025-01-01T10:00:00"
        },
        "quick-scan": {
            "command": "scan", 
            "args": {"recursive": True},
            "description": "Recursive directory scan",
            "created": "2025-01-01T11:00:00"
        }
    }


@pytest.fixture 
def sample_workflows():
    """Sample workflows data for testing."""
    return {
        "process-and-export": [
            {"command": "process", "args": {"backup": True}},
            {"command": "export", "args": {"format": "json"}}
        ],
        "full-pipeline": [
            {"command": "scan", "args": {"recursive": True}},
            {"command": "process", "args": {"parallel": True}},
            {"command": "export", "args": {"format": "json", "compress": True}}
        ]
    }
