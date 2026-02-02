"""
Utility functions for managing artifacts and tracking.

This module provides helper functions for artifact management, including
tracking which artifacts come from the package registry vs user-created ones.
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Dict, Optional, List


# Tracking file to store metadata about artifacts
TRACKING_FILE = ".cuco-tracking.json"


def get_project_root() -> Path:
    """
    Get the project root directory (current working directory).
    
    Returns:
        Path to the project root
    """
    return Path.cwd()


def get_target_dir() -> Path:
    """
    Get the target directory path for customizations.
    
    Checks for integration directories in order:
    1. .github (GitHub Copilot)
    2. .claude (Claude Code)
    3. .cuco (tool-agnostic)
    
    Returns:
        Path to the target directory (defaults to .github if none exist)
    """
    project_root = get_project_root()
    
    # Check for existing directories in priority order
    for dir_name in [".github", ".claude", ".cuco"]:
        target_dir = project_root / dir_name
        if target_dir.exists():
            return target_dir
    
    # Default to .github
    return project_root / ".github"


def get_github_dir() -> Path:
    """
    Get the .github directory path.
    
    Returns:
        Path to .github directory
    """
    return get_project_root() / ".github"


def get_tracking_file_path() -> Path:
    """
    Get the path to the tracking file.
    
    Returns:
        Path to the tracking file
    """
    return get_github_dir() / TRACKING_FILE


def load_tracking_data() -> Dict:
    """
    Load tracking data from the tracking file.
    
    Returns:
        Dictionary containing tracking data
    """
    tracking_file = get_tracking_file_path()
    if tracking_file.exists():
        with open(tracking_file, 'r') as f:
            return json.load(f)
    return {"artifacts": {}}


def save_tracking_data(data: Dict) -> None:
    """
    Save tracking data to the tracking file.
    
    Args:
        data: Dictionary containing tracking data
    """
    tracking_file = get_tracking_file_path()
    tracking_file.parent.mkdir(parents=True, exist_ok=True)
    with open(tracking_file, 'w') as f:
        json.dump(data, f, indent=2)


def calculate_file_hash(file_path: Path) -> str:
    """
    Calculate SHA256 hash of a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Hex digest of the file hash
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def calculate_dir_hash(dir_path: Path) -> str:
    """
    Calculate combined hash of all files in a directory.
    
    Args:
        dir_path: Path to the directory
        
    Returns:
        Hex digest of combined hash
    """
    sha256_hash = hashlib.sha256()
    
    # Sort files for consistent hashing
    for file_path in sorted(dir_path.rglob("*")):
        if file_path.is_file():
            relative_path = file_path.relative_to(dir_path)
            sha256_hash.update(str(relative_path).encode())
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
    
    return sha256_hash.hexdigest()


def track_artifact(
    artifact_type: str,
    artifact_name: str,
    source_hash: str,
    version: str = "latest"
) -> None:
    """
    Track an artifact in the tracking file.
    
    Args:
        artifact_type: Type of artifact (agent, prompt, instructions, skill)
        artifact_name: Name of the artifact
        source_hash: Hash of the source artifact from registry
        version: Version of the artifact
    """
    tracking_data = load_tracking_data()
    
    artifact_key = f"{artifact_type}/{artifact_name}"
    tracking_data["artifacts"][artifact_key] = {
        "type": artifact_type,
        "name": artifact_name,
        "source_hash": source_hash,
        "version": version,
        "from_registry": True
    }
    
    save_tracking_data(tracking_data)


def get_artifact_info(artifact_type: str, artifact_name: str) -> Optional[Dict]:
    """
    Get tracking information for an artifact.
    
    Args:
        artifact_type: Type of artifact
        artifact_name: Name of the artifact
        
    Returns:
        Dictionary with artifact info or None if not tracked
    """
    tracking_data = load_tracking_data()
    artifact_key = f"{artifact_type}/{artifact_name}"
    return tracking_data["artifacts"].get(artifact_key)


def is_artifact_modified(artifact_type: str, artifact_name: str, current_hash: str) -> bool:
    """
    Check if an artifact has been modified since it was added.
    
    Args:
        artifact_type: Type of artifact
        artifact_name: Name of the artifact
        current_hash: Current hash of the artifact
        
    Returns:
        True if modified, False otherwise
    """
    info = get_artifact_info(artifact_type, artifact_name)
    if not info:
        return False
    
    return current_hash != info.get("source_hash")


def get_all_tracked_artifacts() -> List[Dict]:
    """
    Get all tracked artifacts.
    
    Returns:
        List of artifact info dictionaries
    """
    tracking_data = load_tracking_data()
    return list(tracking_data["artifacts"].values())


def get_registry_path() -> Path:
    """
    Get the path to the package registry.
    
    Returns:
        Path to the registry directory
    """
    # This will be the registry directory bundled with the package
    package_dir = Path(__file__).parent
    return package_dir / "registry"
