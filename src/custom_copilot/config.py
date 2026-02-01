"""
Configuration management for custom-copilot.

This module handles configuration including custom source repositories
for private bundles and customizations.
"""

import json
import os
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
