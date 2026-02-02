"""
Pytest configuration and fixtures for custom-copilot tests.
"""

import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    # Cleanup
    if temp_path.exists():
        shutil.rmtree(temp_path)


@pytest.fixture
def mock_cwd(temp_dir, monkeypatch):
    """Mock the current working directory."""
    monkeypatch.chdir(temp_dir)
    return temp_dir


@pytest.fixture
def templates_dir():
    """Get the path to the templates directory."""
    # Assuming tests run from repo root
    return Path(__file__).parent.parent / "custom_copilot" / "templates"
