"""
MCP command - Add MCP servers from registry.

This module implements the `cuco add mcp` command which copies MCP server
configurations from the registry and handles environment variable setup.
"""

import json
import re
import shutil
from pathlib import Path
from typing import List, Dict, Set, Optional
from cc.utils import (
    get_github_dir,
    get_registry_path,
    track_artifact,
    calculate_file_hash,
    get_project_root
)


def extract_env_variables(mcp_config: Dict) -> Set[str]:
    """
    Extract environment variable names from MCP configuration.
    
    Looks for ${env:VARIABLE_NAME} patterns in the configuration.
    
    Args:
        mcp_config: MCP server configuration dictionary
        
    Returns:
        Set of environment variable names
    """
    env_vars = set()
    
    # Convert config to JSON string to search for env patterns
    config_str = json.dumps(mcp_config)
    
    # Find all ${env:VARIABLE_NAME} patterns
    pattern = r'\$\{env:([A-Z_][A-Z0-9_]*)\}'
    matches = re.findall(pattern, config_str)
    
    env_vars.update(matches)
    
    return env_vars


def get_mcp_registry_path() -> Path:
    """
    Get the path to the MCP registry file.
    
    Returns:
        Path to mcp.json in registry
    """
    return get_registry_path() / "mcps" / "mcp.json"


def load_mcp_registry() -> Dict:
    """
    Load the MCP registry file.
    
    Returns:
        Dictionary containing MCP server configurations
    """
    registry_file = get_mcp_registry_path()
    if not registry_file.exists():
        return {"servers": {}}
    
    with open(registry_file, 'r') as f:
        return json.load(f)


def get_project_mcp_file() -> Path:
    """
    Get the path to the project's MCP configuration file.
    
    Returns:
        Path to .vscode/mcp.json in project
    """
    return get_project_root() / ".vscode" / "mcp.json"


def load_project_mcp() -> Dict:
    """
    Load the project's MCP configuration.
    
    Returns:
        Dictionary containing MCP server configurations
    """
    mcp_file = get_project_mcp_file()
    if not mcp_file.exists():
        return {"servers": {}}
    
    with open(mcp_file, 'r') as f:
        return json.load(f)


def save_project_mcp(config: Dict) -> None:
    """
    Save the project's MCP configuration.
    
    Args:
        config: MCP configuration dictionary
    """
    mcp_file = get_project_mcp_file()
    mcp_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(mcp_file, 'w') as f:
        json.dump(config, f, indent=2)


def get_env_file_path() -> Path:
    """
    Get the path to the project's .env file.
    
    Returns:
        Path to .env file
    """
    return get_project_root() / ".env"


def update_env_file(env_vars: Set[str]) -> None:
    """
    Update the .env file with new environment variables.
    
    Creates the file if it doesn't exist, otherwise appends missing variables.
    
    Args:
        env_vars: Set of environment variable names to add
    """
    if not env_vars:
        return
    
    env_file = get_env_file_path()
    
    # Read existing variables
    existing_vars = set()
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    var_name = line.split('=')[0].strip()
                    existing_vars.add(var_name)
    
    # Find variables that need to be added
    new_vars = env_vars - existing_vars
    
    if not new_vars:
        print(f"  All environment variables already exist in {env_file.name}")
        return
    
    # Append new variables
    mode = 'a' if env_file.exists() else 'w'
    with open(env_file, mode) as f:
        if mode == 'a':
            f.write('\n')  # Add blank line before new vars
        
        f.write(f'# Environment variables for MCP servers\n')
        for var in sorted(new_vars):
            f.write(f'{var}=\n')
    
    if mode == 'w':
        print(f"✓ Created {env_file.name}")
    else:
        print(f"✓ Updated {env_file.name}")
    
    print(f"  Added variables: {', '.join(sorted(new_vars))}")
    print(f"  Please set values for these variables in {env_file.name}")


def add_mcp_server(mcp_name: str) -> bool:
    """
    Add an MCP server from the registry.
    
    Args:
        mcp_name: Name of the MCP server
        
    Returns:
        True if successful, False otherwise
    """
    # Load registry
    registry = load_mcp_registry()
    
    if mcp_name not in registry.get("servers", {}):
        print(f"Error: MCP server '{mcp_name}' not found in registry")
        print(f"\nAvailable MCP servers:")
        for name in sorted(registry.get("servers", {}).keys()):
            print(f"  - {name}")
        return False
    
    mcp_config = registry["servers"][mcp_name]
    
    # Load project MCP config
    project_mcp = load_project_mcp()
    
    # Check if already exists
    if mcp_name in project_mcp.get("servers", {}):
        response = input(f"MCP server '{mcp_name}' already exists. Overwrite? [y/N]: ")
        if response.lower() != 'y':
            print("Cancelled.")
            return False
    
    # Extract environment variables
    env_vars = extract_env_variables(mcp_config)
    
    # Add to project configuration
    if "servers" not in project_mcp:
        project_mcp["servers"] = {}
    
    project_mcp["servers"][mcp_name] = mcp_config
    
    # Save configuration
    save_project_mcp(project_mcp)
    
    print(f"✓ Added MCP server '{mcp_name}' to .vscode/mcp.json")
    
    # Update .env file if needed
    if env_vars:
        print(f"\nDetected environment variables: {', '.join(sorted(env_vars))}")
        update_env_file(env_vars)
    
    # Track the artifact
    mcp_registry_file = get_mcp_registry_path()
    if mcp_registry_file.exists():
        source_hash = calculate_file_hash(mcp_registry_file)
        track_artifact("mcps", mcp_name, source_hash)
    
    return True


def run(args: List[str]) -> int:
    """
    Run the MCP add command.
    
    Args:
        args: Command arguments [mcp_name]
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    if len(args) < 1:
        print("Error: Missing MCP name")
        print("Usage: cuco add mcp <name>")
        print("\nAvailable MCP servers:")
        registry = load_mcp_registry()
        for name in sorted(registry.get("servers", {}).keys()):
            print(f"  - {name}")
        return 1
    
    mcp_name = args[0]
    
    if add_mcp_server(mcp_name):
        return 0
    else:
        return 1
