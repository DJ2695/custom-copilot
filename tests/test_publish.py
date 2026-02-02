"""
Tests for the publish command.
"""

import pytest
from pathlib import Path
from custom_copilot.commands import publish


class TestPublishCommand:
    """Test suite for publish command."""
    
    def test_publish_help(self, capsys):
        """Test help output for publish command."""
        result = publish.run(["--help"])
        
        assert result == 0
        captured = capsys.readouterr()
        assert "marketplace" in captured.out
        assert "git-commit" in captured.out
        assert "local" in captured.out
    
    def test_validate_agent_resource(self, mock_cwd):
        """Test validation of agent resources."""
        # Create a valid agent file
        agent_file = mock_cwd / "test-agent.agent.md"
        agent_file.write_text("# Test Agent\n---\nname: test\n---\nContent")
        
        result = publish.validate_resource(agent_file, "agent")
        assert result is True
    
    def test_validate_agent_wrong_extension(self, mock_cwd):
        """Test validation fails for agent with wrong extension."""
        # Create file with wrong extension
        agent_file = mock_cwd / "test-agent.md"
        agent_file.write_text("# Test Agent")
        
        result = publish.validate_resource(agent_file, "agent")
        assert result is False
    
    def test_validate_prompt_resource(self, mock_cwd):
        """Test validation of prompt resources."""
        # Create a valid prompt file
        prompt_file = mock_cwd / "test-prompt.prompt.md"
        prompt_file.write_text("# Test Prompt\nContent")
        
        result = publish.validate_resource(prompt_file, "prompt")
        assert result is True
    
    def test_validate_skill_resource(self, mock_cwd):
        """Test validation of skill resources."""
        # Create a valid skill directory
        skill_dir = mock_cwd / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("# Test Skill")
        
        result = publish.validate_resource(skill_dir, "skill")
        assert result is True
    
    def test_validate_skill_missing_skill_md(self, mock_cwd):
        """Test validation fails for skill without SKILL.md."""
        # Create skill directory without SKILL.md
        skill_dir = mock_cwd / "test-skill"
        skill_dir.mkdir()
        
        result = publish.validate_resource(skill_dir, "skill")
        assert result is False
    
    def test_validate_bundle_resource(self, mock_cwd):
        """Test validation of bundle resources."""
        # Create a valid bundle directory
        bundle_dir = mock_cwd / "test-bundle"
        bundle_dir.mkdir()
        bundle_json = bundle_dir / "bundle.json"
        bundle_json.write_text('{"name": "test", "version": "1.0.0"}')
        
        result = publish.validate_resource(bundle_dir, "bundle")
        assert result is True
    
    def test_validate_bundle_invalid_json(self, mock_cwd):
        """Test validation fails for bundle with invalid JSON."""
        # Create bundle with invalid JSON
        bundle_dir = mock_cwd / "test-bundle"
        bundle_dir.mkdir()
        bundle_json = bundle_dir / "bundle.json"
        bundle_json.write_text('{"name": invalid}')
        
        result = publish.validate_resource(bundle_dir, "bundle")
        assert result is False
    
    def test_publish_marketplace_instructions(self, mock_cwd, capsys):
        """Test marketplace publish provides instructions."""
        # Create a skill
        skill_dir = mock_cwd / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("# Test")
        
        result = publish.run([str(skill_dir), "--type=skill", "--source=marketplace"])
        
        assert result == 0
        captured = capsys.readouterr()
        assert "marketplace" in captured.out.lower()
        assert "fork" in captured.out.lower()
        assert "pull request" in captured.out.lower()
    
    def test_publish_local_destination(self, mock_cwd):
        """Test publishing to local destination."""
        # Create a skill
        skill_dir = mock_cwd / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("# Test")
        
        dest_dir = mock_cwd / "destination"
        dest_dir.mkdir()
        
        result = publish.run([
            str(skill_dir),
            "--type=skill",
            "--source=local",
            f"--destination={dest_dir / 'test-skill'}"
        ])
        
        assert result == 0
        assert (dest_dir / "test-skill").exists()
        assert (dest_dir / "test-skill" / "SKILL.md").exists()
    
    def test_publish_missing_destination(self, mock_cwd):
        """Test error when destination is required but missing."""
        # Create a skill
        skill_dir = mock_cwd / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("# Test")
        
        result = publish.run([str(skill_dir), "--type=skill", "--source=local"])
        
        assert result == 1
    
    def test_publish_resource_not_found(self, mock_cwd):
        """Test error when resource doesn't exist."""
        result = publish.run(["/nonexistent/path", "--type=skill", "--source=marketplace"])
        
        assert result == 1
    
    def test_publish_infer_type_agent(self, mock_cwd, capsys):
        """Test automatic type inference for agent files."""
        agent_file = mock_cwd / "test.agent.md"
        agent_file.write_text("# Test Agent")
        
        result = publish.run([str(agent_file), "--source=marketplace"])
        
        assert result == 0
        captured = capsys.readouterr()
        assert "agent" in captured.out.lower()
    
    def test_publish_infer_type_prompt(self, mock_cwd, capsys):
        """Test automatic type inference for prompt files."""
        prompt_file = mock_cwd / "test.prompt.md"
        prompt_file.write_text("# Test Prompt")
        
        result = publish.run([str(prompt_file), "--source=marketplace"])
        
        assert result == 0
        captured = capsys.readouterr()
        assert "prompt" in captured.out.lower()
    
    def test_publish_infer_type_skill(self, mock_cwd, capsys):
        """Test automatic type inference for skill directories."""
        skill_dir = mock_cwd / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("# Test")
        
        result = publish.run([str(skill_dir), "--source=marketplace"])
        
        assert result == 0
        captured = capsys.readouterr()
        assert "skill" in captured.out.lower()
