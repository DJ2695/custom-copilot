"""
Add command - Add artifacts from the registry.

This module implements the `cuco add` command which copies artifacts from
the package registry to the project's .github directory.
"""

import shutil
from pathlib import Path
from typing import List
from cc.utils import (
    get_github_dir,
    get_registry_path,
    track_artifact,
    calculate_file_hash,
    calculate_dir_hash
)
from cc.commands import mcp


def list_available_artifacts(artifact_type: str) -> List[str]:
    """
    List available artifacts of a given type in the registry.
    
    Args:
        artifact_type: Type of artifact (agents, prompts, instructions, skills)
        
    Returns:
        List of artifact names
    """
    registry_path = get_registry_path() / artifact_type
    if not registry_path.exists():
        return []
    
    artifacts = []
    for item in registry_path.iterdir():
        if item.is_dir() or item.is_file():
            # Remove file extension for files
            name = item.stem if item.is_file() else item.name
            artifacts.append(name)
    
    return sorted(artifacts)


def copy_artifact(artifact_type: str, artifact_name: str) -> bool:
    """
    Copy an artifact from the registry to the project.
    
    Args:
        artifact_type: Type of artifact (agents, prompts, instructions, skills)
        artifact_name: Name of the artifact
        
    Returns:
        True if successful, False otherwise
    """
    registry_path = get_registry_path()
    source_dir = registry_path / artifact_type
    dest_dir = get_github_dir() / artifact_type
    
    # Ensure destination directory exists
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine source path (could be file or directory)
    source_path = None
    possible_paths = [
        source_dir / artifact_name,  # Directory
        source_dir / f"{artifact_name}.md",  # Markdown file
        source_dir / f"{artifact_name}.agent.md",  # Agent file
        source_dir / f"{artifact_name}.prompt.md",  # Prompt file
    ]
    
    for path in possible_paths:
        if path.exists():
            source_path = path
            break
    
    if not source_path:
        print(f"Error: Artifact '{artifact_name}' not found in registry")
        print(f"\nAvailable {artifact_type}:")
        available = list_available_artifacts(artifact_type)
        for item in available:
            print(f"  - {item}")
        return False
    
    # Determine destination path
    if source_path.is_dir():
        dest_path = dest_dir / artifact_name
    else:
        dest_path = dest_dir / source_path.name
    
    # Check if artifact already exists
    if dest_path.exists():
        response = input(f"Artifact '{artifact_name}' already exists. Overwrite? [y/N]: ")
        if response.lower() != 'y':
            print("Cancelled.")
            return False
    
    # Copy the artifact
    try:
        if source_path.is_dir():
            if dest_path.exists():
                shutil.rmtree(dest_path)
            shutil.copytree(source_path, dest_path)
            source_hash = calculate_dir_hash(source_path)
        else:
            shutil.copy2(source_path, dest_path)
            source_hash = calculate_file_hash(source_path)
        
        # Track the artifact
        track_artifact(artifact_type, artifact_name, source_hash)
        
        print(f"✓ Added {artifact_type[:-1]} '{artifact_name}' to .github/{artifact_type}/")
        return True
        
    except Exception as e:
        print(f"Error copying artifact: {e}")
        return False


def run(args: List[str]) -> int:
    """
    Run the add command.
    
    Args:
        args: Command arguments [artifact_type, artifact_name]
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    if len(args) < 1:
        print("Error: Missing artifact type")
        print("Usage: cuco add <type> <name>")
        print("Types: agent, prompt, instructions, skill, mcp")
        return 1
    
    artifact_type_singular = args[0]
    
    # Handle MCP separately
    if artifact_type_singular == "mcp":
        return mcp.run(args[1:])
    
    if len(args) < 2:
        print("Error: Missing artifact name")
        print("Usage: cuco add <type> <name>")
        print("Types: agent, prompt, instructions, skill, mcp")
        return 1
    
    artifact_name = args[1]
    
    # Convert singular to plural for directory names
    type_mapping = {
        "agent": "agents",
        "prompt": "prompts",
        "instructions": "instructions",
        "skill": "skills"
    }
    
    if artifact_type_singular not in type_mapping:
        print(f"Error: Unknown artifact type '{artifact_type_singular}'")
        print("Valid types: agent, prompt, instructions, skill, mcp")
        return 1
    
    artifact_type = type_mapping[artifact_type_singular]
    
    # Check if .github directory exists
    if not get_github_dir().exists():
        print("Error: .github directory not found")
        print("Run 'cuco init' first to initialize the structure")
        return 1
    
    # Copy the artifact
    if copy_artifact(artifact_type, artifact_name):
        return 0
    else:
        return 1
