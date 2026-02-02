"""
Tests for configuration functions.
"""

import pytest
from pathlib import Path
from custom_copilot import config


class TestConfig:
    """Test suite for configuration functions."""
    
    def test_get_custom_source_path_detects_claude(self, mock_cwd, monkeypatch):
        """Test that get_custom_source_path detects .claude folder."""
        # Create a mock repository with .claude structure
        repo_path = mock_cwd / "test_repo"
        claude_dir = repo_path / ".claude"
        claude_dir.mkdir(parents=True)
        (claude_dir / "agents").mkdir()
        
        # Mock the source and repo path
        def mock_get_source_by_name(name):
            return {"name": "test", "type": "git", "url": "test"}
        
        def mock_clone_or_update_repo(source):
            return repo_path
        
        monkeypatch.setattr(config, "get_source_by_name", mock_get_source_by_name)
        monkeypatch.setattr(config, "clone_or_update_repo", mock_clone_or_update_repo)
        
        result = config.get_custom_source_path("test")
        assert result == claude_dir
    
    def test_get_custom_source_path_detects_cuco(self, mock_cwd, monkeypatch):
        """Test that get_custom_source_path detects .cuco folder."""
        repo_path = mock_cwd / "test_repo"
        cuco_dir = repo_path / ".cuco"
        cuco_dir.mkdir(parents=True)
        (cuco_dir / "agents").mkdir()
        
        def mock_get_source_by_name(name):
            return {"name": "test", "type": "git", "url": "test"}
        
        def mock_clone_or_update_repo(source):
            return repo_path
        
        monkeypatch.setattr(config, "get_source_by_name", mock_get_source_by_name)
        monkeypatch.setattr(config, "clone_or_update_repo", mock_clone_or_update_repo)
        
        result = config.get_custom_source_path("test")
        assert result == cuco_dir
    
    def test_get_custom_source_path_detects_github(self, mock_cwd, monkeypatch):
        """Test that get_custom_source_path detects .github folder."""
        repo_path = mock_cwd / "test_repo"
        github_dir = repo_path / ".github"
        github_dir.mkdir(parents=True)
        (github_dir / "agents").mkdir()
        
        def mock_get_source_by_name(name):
            return {"name": "test", "type": "git", "url": "test"}
        
        def mock_clone_or_update_repo(source):
            return repo_path
        
        monkeypatch.setattr(config, "get_source_by_name", mock_get_source_by_name)
        monkeypatch.setattr(config, "clone_or_update_repo", mock_clone_or_update_repo)
        
        result = config.get_custom_source_path("test")
        assert result == github_dir
    
    def test_get_custom_source_path_priority_order(self, mock_cwd, monkeypatch):
        """Test that custom_copilot/ has priority over .cuco/."""
        repo_path = mock_cwd / "test_repo"
        custom_copilot_dir = repo_path / "custom_copilot"
        cuco_dir = repo_path / ".cuco"
        
        # Create both directories
        custom_copilot_dir.mkdir(parents=True)
        cuco_dir.mkdir(parents=True)
        
        def mock_get_source_by_name(name):
            return {"name": "test", "type": "git", "url": "test"}
        
        def mock_clone_or_update_repo(source):
            return repo_path
        
        monkeypatch.setattr(config, "get_source_by_name", mock_get_source_by_name)
        monkeypatch.setattr(config, "clone_or_update_repo", mock_clone_or_update_repo)
        
        result = config.get_custom_source_path("test")
        # custom_copilot should have priority
        assert result == custom_copilot_dir
    
    def test_get_repos_cache_path(self, mock_cwd):
        """Test get_repos_cache_path returns correct path."""
        cache_path = config.get_repos_cache_path()
        assert cache_path == Path.home() / ".cuco" / "repos"
        assert cache_path.exists()  # Should create it
    
    def test_parse_github_url_blob(self):
        """Test parsing GitHub blob URLs."""
        url = "https://github.com/owner/repo/blob/main/path/to/file.md"
        result = config.parse_github_url(url)
        
        assert result is not None
        assert result["owner"] == "owner"
        assert result["repo"] == "repo"
        assert result["ref"] == "main"
        assert result["path"] == "path/to/file.md"
    
    def test_parse_github_url_tree(self):
        """Test parsing GitHub tree URLs."""
        url = "https://github.com/owner/repo/tree/main/path/to/folder"
        result = config.parse_github_url(url)
        
        assert result is not None
        assert result["owner"] == "owner"
        assert result["repo"] == "repo"
        assert result["ref"] == "main"
        assert result["path"] == "path/to/folder"
    
    def test_parse_github_url_raw(self):
        """Test parsing raw.githubusercontent.com URLs."""
        url = "https://raw.githubusercontent.com/owner/repo/main/file.md"
        result = config.parse_github_url(url)
        
        assert result is not None
        assert result["owner"] == "owner"
        assert result["repo"] == "repo"
        assert result["ref"] == "main"
        assert result["path"] == "file.md"
    
    def test_parse_github_url_invalid(self):
        """Test parsing invalid URLs returns None."""
        url = "https://not-github.com/something"
        result = config.parse_github_url(url)
        
        assert result is None
    
    def test_is_agentskills_repo_true(self, mock_cwd):
        """Test is_agentskills_repo returns True for valid agentskills repos."""
        repo_path = mock_cwd / "test_repo"
        skills_dir = repo_path / "skills"
        skill1 = skills_dir / "skill1"
        skill1.mkdir(parents=True)
        (skill1 / "SKILL.md").write_text("# Skill 1")
        
        result = config.is_agentskills_repo(repo_path)
        assert result is True
    
    def test_is_agentskills_repo_false_no_skills_dir(self, mock_cwd):
        """Test is_agentskills_repo returns False when no skills/ dir."""
        repo_path = mock_cwd / "test_repo"
        repo_path.mkdir()
        
        result = config.is_agentskills_repo(repo_path)
        assert result is False
    
    def test_is_agentskills_repo_false_no_skill_md(self, mock_cwd):
        """Test is_agentskills_repo returns False when no SKILL.md files."""
        repo_path = mock_cwd / "test_repo"
        skills_dir = repo_path / "skills"
        skill1 = skills_dir / "skill1"
        skill1.mkdir(parents=True)
        # No SKILL.md file
        
        result = config.is_agentskills_repo(repo_path)
        assert result is False
