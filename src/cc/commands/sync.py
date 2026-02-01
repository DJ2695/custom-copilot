"""
Sync command - Sync artifacts with the registry.

This module implements the `cc sync` command which checks for updates
to artifacts from the registry and handles conflicts with local modifications.
"""

import shutil
from pathlib import Path
from typing import List, Optional
from cc.utils import (
    get_github_dir,
    get_registry_path,
    get_all_tracked_artifacts,
    get_artifact_info,
    is_artifact_modified,
    calculate_file_hash,
    calculate_dir_hash,
    track_artifact
)


def get_current_artifact_hash(artifact_type: str, artifact_name: str) -> Optional[str]:
    """
    Get the current hash of an artifact in the project.
    
    Args:
        artifact_type: Type of artifact
        artifact_name: Name of the artifact
        
    Returns:
        Hash string or None if artifact doesn't exist
    """
    github_dir = get_github_dir()
    artifact_dir = github_dir / artifact_type
    
    # Try different possible paths
    possible_paths = [
        artifact_dir / artifact_name,  # Directory
        artifact_dir / f"{artifact_name}.md",
        artifact_dir / f"{artifact_name}.agent.md",
        artifact_dir / f"{artifact_name}.prompt.md",
    ]
    
    for path in possible_paths:
        if path.exists():
            if path.is_dir():
                return calculate_dir_hash(path)
            else:
                return calculate_file_hash(path)
    
    return None


def get_registry_artifact_hash(artifact_type: str, artifact_name: str) -> Optional[str]:
    """
    Get the hash of an artifact in the registry.
    
    Args:
        artifact_type: Type of artifact
        artifact_name: Name of the artifact
        
    Returns:
        Hash string or None if artifact doesn't exist
    """
    registry_path = get_registry_path() / artifact_type
    
    # Try different possible paths
    possible_paths = [
        registry_path / artifact_name,  # Directory
        registry_path / f"{artifact_name}.md",
        registry_path / f"{artifact_name}.agent.md",
        registry_path / f"{artifact_name}.prompt.md",
    ]
    
    for path in possible_paths:
        if path.exists():
            if path.is_dir():
                return calculate_dir_hash(path)
            else:
                return calculate_file_hash(path)
    
    return None


def sync_artifact(artifact_type: str, artifact_name: str, force: bool = False) -> bool:
    """
    Sync a single artifact with the registry.
    
    Args:
        artifact_type: Type of artifact
        artifact_name: Name of the artifact
        force: If True, skip modification check
        
    Returns:
        True if synced successfully, False otherwise
    """
    # Get artifact info
    info = get_artifact_info(artifact_type, artifact_name)
    if not info:
        print(f"Warning: '{artifact_name}' is not tracked (not from registry)")
        return False
    
    # Get current and registry hashes
    current_hash = get_current_artifact_hash(artifact_type, artifact_name)
    registry_hash = get_registry_artifact_hash(artifact_type, artifact_name)
    
    if not current_hash:
        print(f"Warning: '{artifact_name}' not found in project")
        return False
    
    if not registry_hash:
        print(f"Warning: '{artifact_name}' not found in registry")
        return False
    
    # Check if already up to date
    if registry_hash == info.get("source_hash"):
        print(f"✓ '{artifact_name}' is up to date")
        return True
    
    # Check for local modifications
    is_modified = current_hash != info.get("source_hash")
    
    if is_modified and not force:
        print(f"\n'{artifact_name}' has local modifications.")
        print("Options:")
        print("  1. Overwrite with registry version (local changes will be lost)")
        print("  2. Keep local version (skip sync)")
        print("  3. Show differences (not implemented yet)")
        
        while True:
            choice = input("Choose [1/2]: ").strip()
            if choice == "1":
                break
            elif choice == "2":
                print("Skipped.")
                return False
            else:
                print("Invalid choice. Please enter 1 or 2.")
    
    # Copy from registry
    registry_path = get_registry_path() / artifact_type
    github_dir = get_github_dir() / artifact_type
    
    # Find source path
    source_path = None
    possible_paths = [
        registry_path / artifact_name,
        registry_path / f"{artifact_name}.md",
        registry_path / f"{artifact_name}.agent.md",
        registry_path / f"{artifact_name}.prompt.md",
    ]
    
    for path in possible_paths:
        if path.exists():
            source_path = path
            break
    
    if not source_path:
        print(f"Error: Could not find artifact in registry")
        return False
    
    # Determine destination
    if source_path.is_dir():
        dest_path = github_dir / artifact_name
        if dest_path.exists():
            shutil.rmtree(dest_path)
        shutil.copytree(source_path, dest_path)
    else:
        dest_path = github_dir / source_path.name
        shutil.copy2(source_path, dest_path)
    
    # Update tracking
    track_artifact(artifact_type, artifact_name, registry_hash)
    
    print(f"✓ Synced '{artifact_name}'")
    return True


def run(args: List[str]) -> int:
    """
    Run the sync command.
    
    Args:
        args: Command arguments (optional artifact name)
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Check if .github directory exists
    if not get_github_dir().exists():
        print("Error: .github directory not found")
        print("Run 'cc init' first to initialize the structure")
        return 1
    
    # Sync specific artifact
    if len(args) > 0:
        artifact_name = args[0]
        
        # Try to find which type this artifact is
        tracked_artifacts = get_all_tracked_artifacts()
        matching = [a for a in tracked_artifacts if a["name"] == artifact_name]
        
        if not matching:
            print(f"Error: Artifact '{artifact_name}' is not tracked")
            print("Only artifacts added via 'cc add' can be synced")
            return 1
        
        artifact = matching[0]
        if sync_artifact(artifact["type"], artifact["name"]):
            return 0
        else:
            return 1
    
    # Sync all tracked artifacts
    tracked_artifacts = get_all_tracked_artifacts()
    
    if not tracked_artifacts:
        print("No tracked artifacts found.")
        print("Add artifacts using 'cc add' command first.")
        return 0
    
    print(f"Checking {len(tracked_artifacts)} tracked artifact(s)...\n")
    
    synced_count = 0
    for artifact in tracked_artifacts:
        if sync_artifact(artifact["type"], artifact["name"]):
            synced_count += 1
    
    print(f"\nSync complete! ({synced_count}/{len(tracked_artifacts)} synced)")
    return 0
