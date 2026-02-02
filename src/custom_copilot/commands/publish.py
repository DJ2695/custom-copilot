"""
Publish command - Publish resources to various destinations.

This module implements the `cuco publish` command which helps publish
agents, skills, prompts, instructions, and bundles to different sources.
"""

import json
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional
from custom_copilot.utils import get_target_dir


def validate_resource(resource_path: Path, resource_type: str) -> bool:
    """
    Validate a resource before publishing.
    
    Args:
        resource_path: Path to the resource
        resource_type: Type of resource (agent, skill, prompt, instructions, bundle)
        
    Returns:
        True if valid, False otherwise
    """
    if not resource_path.exists():
        print(f"Error: Resource not found at {resource_path}")
        return False
    
    # Type-specific validation
    if resource_type == "agent":
        if not resource_path.suffix == ".md" or not resource_path.name.endswith(".agent.md"):
            print(f"Error: Agent files must end with .agent.md")
            return False
    
    elif resource_type == "prompt":
        if not resource_path.suffix == ".md" or not resource_path.name.endswith(".prompt.md"):
            print(f"Error: Prompt files must end with .prompt.md")
            return False
    
    elif resource_type == "skill":
        if not resource_path.is_dir():
            print(f"Error: Skills must be directories")
            return False
        skill_md = resource_path / "SKILL.md"
        if not skill_md.exists():
            print(f"Error: Skill must contain SKILL.md file")
            return False
    
    elif resource_type == "bundle":
        if not resource_path.is_dir():
            print(f"Error: Bundles must be directories")
            return False
        bundle_json = resource_path / "bundle.json"
        if not bundle_json.exists():
            print(f"Error: Bundle must contain bundle.json manifest")
            return False
        try:
            with open(bundle_json, 'r') as f:
                json.load(f)
        except Exception as e:
            print(f"Error: Invalid bundle.json: {e}")
            return False
    
    print(f"✓ Resource validation passed")
    return True


def publish_to_local(resource_path: Path, destination: Path) -> bool:
    """
    Publish to a local directory or repository.
    
    Args:
        resource_path: Path to resource
        destination: Destination path
        
    Returns:
        True if successful
    """
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        
        if resource_path.is_file():
            shutil.copy2(resource_path, destination)
        else:
            if destination.exists():
                shutil.rmtree(destination)
            shutil.copytree(resource_path, destination)
        
        print(f"✓ Published to {destination}")
        return True
    except Exception as e:
        print(f"Error publishing: {e}")
        return False


def publish_to_git_repo(resource_path: Path, repo_path: Path, target_subdir: str, commit_message: str) -> bool:
    """
    Publish to a git repository with commit.
    
    Args:
        resource_path: Path to resource
        repo_path: Path to git repository
        target_subdir: Subdirectory in repo (e.g., "skills", "agents")
        commit_message: Commit message
        
    Returns:
        True if successful
    """
    try:
        # Copy resource to repo
        dest = repo_path / target_subdir / resource_path.name
        
        if resource_path.is_file():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(resource_path, dest)
        else:
            if dest.exists():
                shutil.rmtree(dest)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(resource_path, dest)
        
        # Git add
        subprocess.run(
            ["git", "-C", str(repo_path), "add", str(dest.relative_to(repo_path))],
            check=True,
            capture_output=True
        )
        
        # Git commit
        subprocess.run(
            ["git", "-C", str(repo_path), "commit", "-m", commit_message],
            check=True,
            capture_output=True
        )
        
        print(f"✓ Committed to git repository")
        print(f"  You can now push changes with: git -C {repo_path} push")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error with git operation: {e.stderr.decode() if e.stderr else str(e)}")
        return False
    except Exception as e:
        print(f"Error publishing to git repo: {e}")
        return False


def run(args: List[str]) -> int:
    """
    Run the publish command.
    
    Args:
        args: Command arguments [resource_path] [--type=<type>] [--destination=<dest>] [--source=<source>]
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    if len(args) == 0 or args[0] in ["help", "--help", "-h"]:
        print("Usage: cuco publish <resource_path> [options]")
        print("\nOptions:")
        print("  --type=<type>              Resource type (agent, skill, prompt, bundle)")
        print("  --destination=<path>       Destination path or repo")
        print("  --source=<type>            Publication source type:")
        print("                             - local: Local directory/file")
        print("                             - git-commit: Git repo with commit")
        print("                             - marketplace: CUCO marketplace (creates PR guide)")
        print("  --message=<msg>            Commit message (for git-commit)")
        print("\nExamples:")
        print("  # Publish to local directory")
        print("  cuco publish ./my-skill --type=skill --destination=/path/to/dest")
        print("  ")
        print("  # Publish to git repository with commit")
        print("  cuco publish ./my-agent.agent.md --type=agent \\")
        print("    --source=git-commit --destination=/path/to/repo/agents \\")
        print("    --message=\"Add new agent\"")
        print("  ")
        print("  # Get instructions for marketplace PR")
        print("  cuco publish ./my-skill --type=skill --source=marketplace")
        return 0
    
    # Parse arguments
    resource_path = Path(args[0])
    resource_type = None
    destination = None
    source_type = "local"
    commit_message = "Publish resource via cuco"
    
    for arg in args[1:]:
        if arg.startswith("--type="):
            resource_type = arg.split("=", 1)[1]
        elif arg.startswith("--destination="):
            destination = Path(arg.split("=", 1)[1])
        elif arg.startswith("--source="):
            source_type = arg.split("=", 1)[1]
        elif arg.startswith("--message="):
            commit_message = arg.split("=", 1)[1]
    
    # Infer resource type from path if not specified
    if resource_type is None:
        if resource_path.suffix == ".md":
            if resource_path.name.endswith(".agent.md"):
                resource_type = "agent"
            elif resource_path.name.endswith(".prompt.md"):
                resource_type = "prompt"
        elif resource_path.is_dir():
            if (resource_path / "SKILL.md").exists():
                resource_type = "skill"
            elif (resource_path / "bundle.json").exists():
                resource_type = "bundle"
        
        if resource_type is None:
            print("Error: Could not infer resource type. Please specify with --type=")
            return 1
    
    print(f"Publishing {resource_type}: {resource_path}")
    
    # Validate resource
    if not validate_resource(resource_path, resource_type):
        return 1
    
    # Handle different source types
    if source_type == "marketplace":
        print("\n" + "=" * 60)
        print("CUCO Marketplace Publication Guide")
        print("=" * 60)
        print("\nTo publish to the CUCO marketplace:")
        print("1. Fork the repository: https://github.com/DJ2695/custom-copilot")
        print("2. Clone your fork locally")
        print(f"3. Copy your {resource_type} to the appropriate directory:")
        if resource_type == "skill":
            print(f"   cp -r {resource_path} custom-copilot/custom_copilot/skills/")
        elif resource_type == "agent":
            print(f"   cp {resource_path} custom-copilot/custom_copilot/agents/")
        elif resource_type == "prompt":
            print(f"   cp {resource_path} custom-copilot/custom_copilot/prompts/")
        elif resource_type == "bundle":
            print(f"   cp -r {resource_path} custom-copilot/custom_copilot/bundles/")
        print("4. Commit your changes")
        print("5. Push to your fork")
        print("6. Create a Pull Request to the main repository")
        print("\nYour contribution will be reviewed by maintainers!")
        return 0
    
    elif source_type == "local":
        if destination is None:
            print("Error: --destination required for local publish")
            return 1
        
        if publish_to_local(resource_path, destination):
            return 0
        else:
            return 1
    
    elif source_type == "git-commit":
        if destination is None:
            print("Error: --destination required for git-commit")
            print("  Specify the target repo path and subdirectory")
            return 1
        
        # Extract repo path and subdir
        # Assume destination is like /path/to/repo/agents
        repo_path = destination
        while not (repo_path / ".git").exists() and repo_path != repo_path.parent:
            repo_path = repo_path.parent
        
        if not (repo_path / ".git").exists():
            print(f"Error: No git repository found at or above {destination}")
            return 1
        
        target_subdir = str(destination.relative_to(repo_path).parent)
        
        if publish_to_git_repo(resource_path, repo_path, target_subdir, commit_message):
            return 0
        else:
            return 1
    
    else:
        print(f"Error: Unknown source type '{source_type}'")
        print("Available: local, git-commit, marketplace")
        return 1
