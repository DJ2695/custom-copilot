"""
List command - List available artifacts from the registry.

This module implements the `cc list` command which shows available artifacts
in the package registry.
"""

import json
from pathlib import Path
from typing import List
from cc.utils import get_registry_path


def list_mcp_servers() -> List[str]:
    """
    List available MCP servers in the registry.
    
    Returns:
        List of MCP server names
    """
    mcp_file = get_registry_path() / "mcps" / "mcp.json"
    if not mcp_file.exists():
        return []
    
    with open(mcp_file, 'r') as f:
        config = json.load(f)
    
    return sorted(config.get("servers", {}).keys())


def list_artifacts(artifact_type: str) -> List[str]:
    """
    List available artifacts of a given type in the registry.
    
    Args:
        artifact_type: Type of artifact (agents, prompts, instructions, skills, mcps)
        
    Returns:
        List of artifact names
    """
    # Handle MCPs specially since they're in a single JSON file
    if artifact_type == "mcps":
        return list_mcp_servers()
    
    registry_path = get_registry_path() / artifact_type
    if not registry_path.exists():
        return []
    
    artifacts = []
    for item in registry_path.iterdir():
        if item.is_dir():
            # For directories (skills), use the directory name
            artifacts.append(item.name)
        elif item.is_file():
            # For files, remove extensions
            name = item.stem
            # Remove type suffix if present (e.g., .agent, .prompt)
            if '.' in name:
                name = name.split('.')[0]
            if name not in artifacts:
                artifacts.append(name)
    
    return sorted(artifacts)


def run(args: List[str]) -> int:
    """
    Run the list command.
    
    Args:
        args: Command arguments [artifact_type]
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    if len(args) < 1:
        print("Error: Missing artifact type")
        print("Usage: cc list <type>")
        print("Types: agents, prompts, instructions, skills, mcps")
        return 1
    
    artifact_type = args[0]
    
    # Validate artifact type
    valid_types = ["agents", "prompts", "instructions", "skills", "mcps"]
    if artifact_type not in valid_types:
        print(f"Error: Unknown artifact type '{artifact_type}'")
        print(f"Valid types: {', '.join(valid_types)}")
        return 1
    
    # Get artifacts
    artifacts = list_artifacts(artifact_type)
    
    if not artifacts:
        print(f"No {artifact_type} found in registry.")
        return 0
    
    print(f"Available {artifact_type}:")
    for artifact in artifacts:
        print(f"  - {artifact}")
    
    print(f"\nTotal: {len(artifacts)} {artifact_type}")
    print(f"\nAdd with: cc add {artifact_type[:-1] if artifact_type != 'mcps' else 'mcp'} <name>")
    
    return 0
