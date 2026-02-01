"""
Configuration management for custom-copilot.

This module handles configuration including custom source repositories
for private bundles and customizations.
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional


def get_config_path() -> Path:
    """
    Get the path to the configuration file.
    
    Checks in order:
    1. .cuco-config.json in current directory
    2. ~/.cuco/config.json in user's home directory
    
    Returns:
        Path to configuration file
    """
    # Check local config first
    local_config = Path.cwd() / ".cuco-config.json"
    if local_config.exists():
        return local_config
    
    # Check user config
    user_config = Path.home() / ".cuco" / "config.json"
    return user_config


def load_config() -> Dict:
    """
    Load configuration from file.
    
    Returns:
        Dictionary with configuration, empty if no config exists
    """
    config_path = get_config_path()
    
    if not config_path.exists():
        return {}
    
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Error loading config from {config_path}: {e}")
        return {}


def save_config(config: Dict) -> None:
    """
    Save configuration to file.
    
    Args:
        config: Configuration dictionary to save
    """
    config_path = get_config_path()
    
    # Create directory if it doesn't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"Error saving config to {config_path}: {e}")


def get_custom_sources() -> List[Dict]:
    """
    Get list of custom source repositories.
    
    Returns:
        List of source dictionaries with 'name', 'type', and 'url' keys
    """
    config = load_config()
    return config.get("sources", [])


def add_custom_source(name: str, source_type: str, url: str) -> bool:
    """
    Add a custom source repository.
    
    Args:
        name: Name identifier for the source
        source_type: Type of source ('git', 'local', etc.)
        url: URL or path to the source
        
    Returns:
        True if successful, False otherwise
    """
    config = load_config()
    
    if "sources" not in config:
        config["sources"] = []
    
    # Check if source already exists
    for source in config["sources"]:
        if source.get("name") == name:
            print(f"Source '{name}' already exists. Updating...")
            source["type"] = source_type
            source["url"] = url
            save_config(config)
            return True
    
    # Add new source
    config["sources"].append({
        "name": name,
        "type": source_type,
        "url": url
    })
    
    save_config(config)
    return True


def remove_custom_source(name: str) -> bool:
    """
    Remove a custom source repository.
    
    Args:
        name: Name identifier of the source to remove
        
    Returns:
        True if successful, False if source not found
    """
    config = load_config()
    
    if "sources" not in config:
        return False
    
    original_length = len(config["sources"])
    config["sources"] = [s for s in config["sources"] if s.get("name") != name]
    
    if len(config["sources"]) < original_length:
        save_config(config)
        return True
    
    return False


def get_source_by_name(name: str) -> Optional[Dict]:
    """
    Get a custom source by name.
    
    Args:
        name: Name identifier of the source
        
    Returns:
        Source dictionary or None if not found
    """
    sources = get_custom_sources()
    for source in sources:
        if source.get("name") == name:
            return source
    return None


def get_repos_cache_path() -> Path:
    """
    Get the path to the repositories cache directory.
    
    Returns:
        Path to ~/.cuco/repos/ directory
    """
    cache_path = Path.home() / ".cuco" / "repos"
    cache_path.mkdir(parents=True, exist_ok=True)
    return cache_path


def get_repo_path(source_name: str) -> Path:
    """
    Get the path where a source repository is cached.
    
    Args:
        source_name: Name of the source
        
    Returns:
        Path to the cached repository
    """
    return get_repos_cache_path() / source_name


def clone_or_update_repo(source: Dict) -> Optional[Path]:
    """
    Clone or update a git repository from a custom source.
    
    Args:
        source: Source dictionary with 'name', 'type', and 'url' keys
        
    Returns:
        Path to the cloned repository, or None if failed
    """
    source_name = source.get("name")
    source_type = source.get("type")
    source_url = source.get("url")
    
    if source_type != "git":
        print(f"Warning: Source '{source_name}' is not a git repository")
        return None
    
    repo_path = get_repo_path(source_name)
    
    try:
        if repo_path.exists():
            # Repository already exists, try to update it
            print(f"Updating repository '{source_name}'...")
            result = subprocess.run(
                ["git", "-C", str(repo_path), "pull"],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode != 0:
                print(f"Warning: Failed to update repository: {result.stderr}")
                # Continue with existing repo even if update fails
            else:
                print(f"✓ Updated repository '{source_name}'")
        else:
            # Clone the repository
            print(f"Cloning repository '{source_name}' from {source_url}...")
            result = subprocess.run(
                ["git", "clone", source_url, str(repo_path)],
                capture_output=True,
                text=True,
                timeout=120
            )
            if result.returncode != 0:
                print(f"Error: Failed to clone repository: {result.stderr}")
                print("\nAuthentication options:")
                print("  1. For HTTPS: Use 'git credential' or set up a personal access token")
                print("  2. For SSH: Ensure your SSH key is added to ssh-agent")
                print(f"  3. Try: ssh-add ~/.ssh/id_rsa (or your key path)")
                return None
            else:
                print(f"✓ Cloned repository '{source_name}'")
        
        return repo_path
    
    except subprocess.TimeoutExpired:
        print(f"Error: Git operation timed out for '{source_name}'")
        return None
    except FileNotFoundError:
        print("Error: Git is not installed or not in PATH")
        return None
    except Exception as e:
        print(f"Error: Failed to clone/update repository: {e}")
        return None


def get_custom_source_path(source_name: str) -> Optional[Path]:
    """
    Get the path to the custom_copilot folder in a custom source repository.
    
    Args:
        source_name: Name of the source
        
    Returns:
        Path to custom_copilot folder in the source, or None if not found
    """
    source = get_source_by_name(source_name)
    if not source:
        return None
    
    repo_path = clone_or_update_repo(source)
    if not repo_path:
        return None
    
    # Look for custom_copilot folder in the repository
    custom_copilot_path = repo_path / "custom_copilot"
    if not custom_copilot_path.exists():
        print(f"Warning: Repository '{source_name}' does not have a custom_copilot folder")
        return None
    
    return custom_copilot_path
