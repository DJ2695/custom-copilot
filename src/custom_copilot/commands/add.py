"""
Add command - Add artifacts from the registry.

This module implements the `cuco add` command which copies artifacts from
the package registry to the project's .github directory.
"""

import shutil
from pathlib import Path
from typing import List
from custom_copilot.utils import (
    get_github_dir,
    get_registry_path,
    track_artifact,
    calculate_file_hash,
    calculate_dir_hash
)
from custom_copilot.commands import mcp
from custom_copilot.config import (
    parse_github_url,
    download_github_file,
    clone_or_update_repo,
    get_repos_cache_path
)


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


def add_from_github_url(url: str, artifact_type: str) -> bool:
    """
    Add an artifact directly from a GitHub URL.
    
    Supports:
    - Direct file URLs (e.g., SKILL.md)
    - Folder URLs (will clone and copy folder)
    - Repository URLs (will auto-detect structure)
    
    Args:
        url: GitHub URL
        artifact_type: Type of artifact (agents, prompts, skills, etc.)
        
    Returns:
        True if successful, False otherwise
    """
    github_info = parse_github_url(url)
    if not github_info:
        print(f"Error: Invalid GitHub URL: {url}")
        return False
    
    owner = github_info["owner"]
    repo = github_info["repo"]
    path = github_info["path"]
    ref = github_info["ref"]
    
    dest_dir = get_github_dir() / artifact_type
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # Valid file extensions for direct file downloads
    VALID_EXTENSIONS = {'.md', '.agent.md', '.prompt.md'}
    
    # Case 1: Direct file URL (e.g., pointing to a SKILL.md file)
    if path and any(path.endswith(ext) for ext in VALID_EXTENSIONS):
        print(f"Downloading {path} from {owner}/{repo}...")
        temp_file = download_github_file(owner, repo, path, ref)
        
        if not temp_file:
            return False
        
        # Determine artifact name from path
        file_name = Path(path).name
        artifact_name = Path(path).parent.name if Path(path).parent.name != "." else Path(path).stem
        
        dest_path = dest_dir / file_name
        
        # Check if artifact already exists
        if dest_path.exists():
            response = input(f"File '{file_name}' already exists. Overwrite? [y/N]: ")
            if response.lower() != 'y':
                temp_file.unlink()
                print("Cancelled.")
                return False
        
        # Copy the file
        shutil.copy2(temp_file, dest_path)
        temp_file.unlink()
        
        print(f"✓ Added {artifact_type[:-1]} from GitHub to .github/{artifact_type}/{file_name}")
        return True
    
    # Case 2: Folder or repository URL - clone and extract
    else:
        print(f"Cloning repository {owner}/{repo}...")
        
        # Create a temporary source entry
        temp_source = {
            "name": f"{owner}_{repo}",
            "type": "git",
            "url": f"https://github.com/{owner}/{repo}.git"
        }
        
        # Clone/update the repo
        repo_path = clone_or_update_repo(temp_source)
        if not repo_path:
            return False
        
        # Determine what to copy based on path
        if path:
            # Specific folder path provided
            source_path = repo_path / path
            if not source_path.exists():
                print(f"Error: Path '{path}' not found in repository")
                return False
            
            artifact_name = source_path.name
            dest_path = dest_dir / artifact_name
            
            if dest_path.exists():
                response = input(f"Artifact '{artifact_name}' already exists. Overwrite? [y/N]: ")
                if response.lower() != 'y':
                    print("Cancelled.")
                    return False
                if dest_path.is_dir():
                    shutil.rmtree(dest_path)
            
            if source_path.is_dir():
                shutil.copytree(source_path, dest_path)
            else:
                shutil.copy2(source_path, dest_path)
            
            print(f"✓ Added {artifact_type[:-1]} '{artifact_name}' from GitHub")
            return True
        else:
            # No specific path - need to auto-detect structure
            print("Auto-detecting repository structure...")
            
            # Check for agentskills.io structure (skills/ folder)
            skills_folder = repo_path / "skills"
            if artifact_type == "skills" and skills_folder.exists():
                print(f"Found agentskills.io structure")
                print(f"Available skills:")
                
                available_skills = []
                for item in skills_folder.iterdir():
                    if item.is_dir() and (item / "SKILL.md").exists():
                        available_skills.append(item.name)
                        print(f"  - {item.name}")
                
                if not available_skills:
                    print("No skills found with SKILL.md files")
                    return False
                
                # For now, return false and tell user to specify the skill
                print(f"\nPlease specify which skill to add:")
                print(f"  cuco add skill {url}/skills/<skill-name>")
                return False
            
            print("Could not auto-detect structure. Please provide a specific path.")
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
    
    # Check if artifact_name is a GitHub URL
    if artifact_name.startswith("http://") or artifact_name.startswith("https://"):
        # Validate it's actually a GitHub URL by checking the domain properly
        if artifact_name.startswith("https://github.com/") or \
           artifact_name.startswith("http://github.com/") or \
           artifact_name.startswith("https://raw.githubusercontent.com/"):
            print(f"Detected GitHub URL, fetching {artifact_type_singular}...")
            if add_from_github_url(artifact_name, artifact_type):
                return 0
            else:
                return 1
        else:
            print("Error: Only GitHub URLs are currently supported")
            print("  Supported formats:")
            print("    - https://github.com/owner/repo/...")
            print("    - https://raw.githubusercontent.com/owner/repo/...")
            return 1
    
    # Copy the artifact from registry
    if copy_artifact(artifact_type, artifact_name):
        return 0
    else:
        return 1
