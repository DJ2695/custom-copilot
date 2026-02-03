"""
Tests for the init command with multi-engine support.
"""

import pytest
from pathlib import Path
from custom_copilot.commands import init


class TestInitCommand:
    """Test suite for init command."""
    
    def test_init_default_github_engine(self, mock_cwd):
        """Test default initialization creates .github folder."""
        result = init.run([])
        
        assert result == 0
        assert (mock_cwd / ".github").exists()
        assert (mock_cwd / ".github" / "agents").exists()
        assert (mock_cwd / ".github" / "prompts").exists()
        assert (mock_cwd / ".github" / "instructions").exists()
        assert (mock_cwd / ".github" / "skills").exists()
        assert (mock_cwd / ".github" / "copilot-instructions.md").exists()
    
    def test_init_claude_engine(self, mock_cwd):
        """Test initialization with Claude engine creates .claude folder."""
        result = init.run(["--engine=claude"])
        
        assert result == 0
        assert (mock_cwd / ".claude").exists()
        assert (mock_cwd / ".claude" / "agents").exists()
        assert (mock_cwd / ".claude" / "prompts").exists()
        assert (mock_cwd / ".claude" / "skills").exists()
        assert (mock_cwd / ".claude" / "instructions.md").exists()
        # .claude should not have instructions subfolder
        assert not (mock_cwd / ".claude" / "instructions").exists()
    
    def test_init_cuco_engine(self, mock_cwd):
        """Test initialization with cuco engine creates .cuco folder."""
        result = init.run(["--engine=cuco"])
        
        assert result == 0
        assert (mock_cwd / ".cuco").exists()
        assert (mock_cwd / ".cuco" / "agents").exists()
        assert (mock_cwd / ".cuco" / "prompts").exists()
        assert (mock_cwd / ".cuco" / "instructions").exists()
        assert (mock_cwd / ".cuco" / "skills").exists()
        assert (mock_cwd / ".cuco" / "bundles").exists()
        assert (mock_cwd / ".cuco" / "mcps").exists()
        assert (mock_cwd / ".cuco" / "config.json").exists()
        
        # Verify config.json content
        import json
        with open(mock_cwd / ".cuco" / "config.json") as f:
            config = json.load(f)
            assert "version" in config
            assert "sources" in config
            assert "integrations" in config
    
    def test_init_invalid_engine(self, mock_cwd):
        """Test initialization with invalid engine returns error."""
        result = init.run(["--engine=invalid"])
        
        assert result == 1
        # No directories should be created
        assert not (mock_cwd / ".github").exists()
        assert not (mock_cwd / ".claude").exists()
        assert not (mock_cwd / ".cuco").exists()
    
    def test_init_help(self, mock_cwd, capsys):
        """Test help output for init command."""
        result = init.run(["--help"])
        
        assert result == 0
        captured = capsys.readouterr()
        assert "github" in captured.out.lower()
        assert "claude" in captured.out.lower()
        assert "cuco" in captured.out.lower()
    
    def test_init_creates_subdirectories(self, mock_cwd):
        """Test that all required subdirectories are created."""
        result = init.run(["--engine=github"])
        
        assert result == 0
        github_dir = mock_cwd / ".github"
        
        # Check all expected subdirectories
        expected_dirs = ["agents", "prompts", "instructions", "skills"]
        for subdir in expected_dirs:
            assert (github_dir / subdir).is_dir()
    
    def test_init_idempotent(self, mock_cwd):
        """Test that running init multiple times is safe."""
        # First run
        result1 = init.run([])
        assert result1 == 0
        
        # Second run - should still succeed
        result2 = init.run([])
        assert result2 == 0
        
        # Structure should still be intact
        assert (mock_cwd / ".github").exists()
        assert (mock_cwd / ".github" / "agents").exists()
