"""
Tests for utility functions.
"""

import pytest
from pathlib import Path
from custom_copilot import utils


class TestUtils:
    """Test suite for utility functions."""
    
    def test_get_target_dir_github_exists(self, mock_cwd):
        """Test get_target_dir returns .github when it exists."""
        github_dir = mock_cwd / ".github"
        github_dir.mkdir()
        
        target = utils.get_target_dir()
        assert target == github_dir
    
    def test_get_target_dir_claude_exists(self, mock_cwd):
        """Test get_target_dir returns .claude when .github doesn't exist."""
        claude_dir = mock_cwd / ".claude"
        claude_dir.mkdir()
        
        target = utils.get_target_dir()
        assert target == claude_dir
    
    def test_get_target_dir_cuco_exists(self, mock_cwd):
        """Test get_target_dir returns .cuco when neither .github nor .claude exist."""
        cuco_dir = mock_cwd / ".cuco"
        cuco_dir.mkdir()
        
        target = utils.get_target_dir()
        assert target == cuco_dir
    
    def test_get_target_dir_priority_github_over_claude(self, mock_cwd):
        """Test get_target_dir prioritizes .github over .claude."""
        github_dir = mock_cwd / ".github"
        claude_dir = mock_cwd / ".claude"
        github_dir.mkdir()
        claude_dir.mkdir()
        
        target = utils.get_target_dir()
        assert target == github_dir
    
    def test_get_target_dir_priority_github_over_cuco(self, mock_cwd):
        """Test get_target_dir prioritizes .github over .cuco."""
        github_dir = mock_cwd / ".github"
        cuco_dir = mock_cwd / ".cuco"
        github_dir.mkdir()
        cuco_dir.mkdir()
        
        target = utils.get_target_dir()
        assert target == github_dir
    
    def test_get_target_dir_priority_claude_over_cuco(self, mock_cwd):
        """Test get_target_dir prioritizes .claude over .cuco."""
        claude_dir = mock_cwd / ".claude"
        cuco_dir = mock_cwd / ".cuco"
        claude_dir.mkdir()
        cuco_dir.mkdir()
        
        target = utils.get_target_dir()
        assert target == claude_dir
    
    def test_get_target_dir_default_github(self, mock_cwd):
        """Test get_target_dir defaults to .github when none exist."""
        target = utils.get_target_dir()
        assert target == mock_cwd / ".github"
    
    def test_get_github_dir(self, mock_cwd):
        """Test get_github_dir always returns .github path."""
        github_dir = utils.get_github_dir()
        assert github_dir == mock_cwd / ".github"
    
    def test_get_project_root(self, mock_cwd):
        """Test get_project_root returns current working directory."""
        root = utils.get_project_root()
        assert root == mock_cwd
    
    def test_calculate_file_hash(self, mock_cwd):
        """Test file hash calculation."""
        test_file = mock_cwd / "test.txt"
        test_file.write_text("test content")
        
        hash1 = utils.calculate_file_hash(test_file)
        assert hash1 is not None
        assert len(hash1) == 64  # SHA256 hex digest length
        
        # Same content should give same hash
        hash2 = utils.calculate_file_hash(test_file)
        assert hash1 == hash2
    
    def test_calculate_file_hash_different_content(self, mock_cwd):
        """Test different files have different hashes."""
        file1 = mock_cwd / "test1.txt"
        file2 = mock_cwd / "test2.txt"
        file1.write_text("content 1")
        file2.write_text("content 2")
        
        hash1 = utils.calculate_file_hash(file1)
        hash2 = utils.calculate_file_hash(file2)
        
        assert hash1 != hash2
    
    def test_calculate_dir_hash(self, mock_cwd):
        """Test directory hash calculation."""
        test_dir = mock_cwd / "test_dir"
        test_dir.mkdir()
        (test_dir / "file1.txt").write_text("content 1")
        (test_dir / "file2.txt").write_text("content 2")
        
        hash1 = utils.calculate_dir_hash(test_dir)
        assert hash1 is not None
        assert len(hash1) == 64
        
        # Same directory should give same hash
        hash2 = utils.calculate_dir_hash(test_dir)
        assert hash1 == hash2
    
    def test_calculate_dir_hash_different_content(self, mock_cwd):
        """Test directory hashes change when content changes."""
        test_dir = mock_cwd / "test_dir"
        test_dir.mkdir()
        (test_dir / "file1.txt").write_text("content 1")
        
        hash1 = utils.calculate_dir_hash(test_dir)
        
        # Add another file
        (test_dir / "file2.txt").write_text("content 2")
        
        hash2 = utils.calculate_dir_hash(test_dir)
        assert hash1 != hash2
