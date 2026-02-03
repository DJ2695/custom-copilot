"""
Tests for the template command.
"""

import pytest
from pathlib import Path
from custom_copilot.commands import template


class TestTemplateCommand:
    """Test suite for template command."""
    
    def test_template_list(self, capsys):
        """Test listing available templates."""
        result = template.run(["list"])
        
        assert result == 0
        captured = capsys.readouterr()
        assert "agent" in captured.out
        assert "skill" in captured.out
        assert "prompt" in captured.out
        assert "bundle" in captured.out
    
    def test_create_agent_template(self, mock_cwd):
        """Test creating an agent template."""
        # Initialize .github first
        (mock_cwd / ".github" / "agents").mkdir(parents=True)
        
        result = template.run(["create", "agent", "test-agent"])
        
        assert result == 0
        agent_file = mock_cwd / ".github" / "agents" / "test-agent.agent.md"
        assert agent_file.exists()
        
        # Verify it's a valid agent file
        content = agent_file.read_text()
        assert "# Agent Template" in content or "agent" in content.lower()
        assert "---" in content  # YAML frontmatter markers
    
    def test_create_skill_template(self, mock_cwd):
        """Test creating a skill template."""
        # Initialize .github first
        (mock_cwd / ".github" / "skills").mkdir(parents=True)
        
        result = template.run(["create", "skill", "test-skill"])
        
        assert result == 0
        skill_dir = mock_cwd / ".github" / "skills" / "test-skill"
        assert skill_dir.exists()
        assert skill_dir.is_dir()
        assert (skill_dir / "SKILL.md").exists()
    
    def test_create_prompt_template(self, mock_cwd):
        """Test creating a prompt template."""
        # Initialize .github first
        (mock_cwd / ".github" / "prompts").mkdir(parents=True)
        
        result = template.run(["create", "prompt", "test-prompt"])
        
        assert result == 0
        prompt_file = mock_cwd / ".github" / "prompts" / "test-prompt.prompt.md"
        assert prompt_file.exists()
    
    def test_create_bundle_template(self, mock_cwd):
        """Test creating a bundle template."""
        # Initialize .github first
        (mock_cwd / ".github" / "bundles").mkdir(parents=True)
        
        result = template.run(["create", "bundle", "test-bundle"])
        
        assert result == 0
        bundle_dir = mock_cwd / ".github" / "bundles" / "test-bundle"
        assert bundle_dir.exists()
        assert bundle_dir.is_dir()
        assert (bundle_dir / "bundle.json").exists()
    
    def test_create_template_invalid_type(self, mock_cwd):
        """Test creating template with invalid type."""
        result = template.run(["create", "invalid", "test"])
        
        assert result == 1
    
    def test_create_template_missing_args(self, mock_cwd):
        """Test error when missing required arguments."""
        result = template.run(["create", "agent"])
        
        assert result == 1
    
    def test_template_help(self, capsys):
        """Test help output for template command."""
        result = template.run(["--help"])
        
        assert result == 0
        captured = capsys.readouterr()
        assert "create" in captured.out
        assert "list" in captured.out
    
    def test_create_in_claude_folder(self, mock_cwd):
        """Test creating template in .claude folder when it exists."""
        # Create .claude structure
        (mock_cwd / ".claude" / "agents").mkdir(parents=True)
        
        result = template.run(["create", "agent", "claude-agent"])
        
        assert result == 0
        # Should create in .claude since it exists
        agent_file = mock_cwd / ".claude" / "agents" / "claude-agent.agent.md"
        assert agent_file.exists()
    
    def test_create_in_cuco_folder(self, mock_cwd):
        """Test creating template in .cuco folder when it exists."""
        # Create .cuco structure
        (mock_cwd / ".cuco" / "skills").mkdir(parents=True)
        
        result = template.run(["create", "skill", "cuco-skill"])
        
        assert result == 0
        # Should create in .cuco since it exists
        skill_dir = mock_cwd / ".cuco" / "skills" / "cuco-skill"
        assert skill_dir.exists()
    
    def test_placeholder_replacement(self, mock_cwd):
        """Test that placeholders are properly replaced in templates."""
        (mock_cwd / ".github" / "agents").mkdir(parents=True)
        
        result = template.run(["create", "agent", "my-custom-agent"])
        
        assert result == 0
        agent_file = mock_cwd / ".github" / "agents" / "my-custom-agent.agent.md"
        content = agent_file.read_text()
        
        # Placeholders should be replaced
        assert "{{NAME}}" not in content
        assert "{{name}}" not in content
