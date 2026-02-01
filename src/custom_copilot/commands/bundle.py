"""
Bundle command - Manage copilot customization bundles.

This module implements bundle operations including listing, adding, and
managing bundles which are pre-configured combinations of copilot customizations.
"""

import json
import shutil
from pathlib import Path
from typing import List, Dict, Optional
from custom_copilot.utils import (
    get_github_dir,
    track_artifact,
    calculate_file_hash,
    calculate_dir_hash
)
from custom_copilot.config import get_custom_source_path


def get_customizations_path() -> Path:
    """
    Get the path to the custom_copilot directory.
    
    Returns:
        Path to custom_copilot directory in the package
    """
    package_dir = Path(__file__).parent.parent
    return package_dir.parent.parent / "custom_copilot"


def list_available_bundles() -> List[str]:
    """
    List available bundles in the customizations directory.
    
    Returns:
        List of bundle names
    """
    bundles_path = get_customizations_path() / "bundles"
    if not bundles_path.exists():
        return []
    
    bundles = []
    for item in bundles_path.iterdir():
        if item.is_dir() and (item / "bundle.json").exists():
            bundles.append(item.name)
    
    return sorted(bundles)


def load_bundle_manifest(bundle_name: str) -> Optional[Dict]:
    """
    Load a bundle manifest file.
    
    Args:
        bundle_name: Name of the bundle
        
    Returns:
        Bundle manifest dictionary or None if not found
    """
    bundle_path = get_customizations_path() / "bundles" / bundle_name
    manifest_path = bundle_path / "bundle.json"
    
    if not manifest_path.exists():
        return None
    
    try:
        with open(manifest_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading bundle manifest: {e}")
        return None


def install_bundle_resource(bundle_path: Path, resource_type: str, resource: Dict, dest_dir: Path) -> bool:
    """
    Install a bundle resource (bundle, custom-copilot, custom, or github).
    
    Args:
        bundle_path: Path to the bundle directory
        resource_type: Type of resource (agents, prompts, skills, instructions)
        resource: Resource definition from bundle manifest
        dest_dir: Destination directory in .github
        
    Returns:
        True if successful, False otherwise
    """
    resource_name = resource.get("name")
    resource_kind = resource.get("type")
    
    if resource_kind == "bundle":
        # Copy from bundle directory (formerly "inline")
        source_path_rel = resource.get("path")
        source_path = bundle_path / source_path_rel
        
        if not source_path.exists():
            print(f"Warning: Bundle resource not found: {source_path}")
            return False
        
        if source_path.is_dir():
            dest_path = dest_dir / resource_name
            if dest_path.exists():
                shutil.rmtree(dest_path)
            shutil.copytree(source_path, dest_path)
        else:
            dest_path = dest_dir / source_path.name
            shutil.copy2(source_path, dest_path)
        
        print(f"  ✓ Installed bundle {resource_type[:-1]} '{resource_name}'")
        return True
        
    elif resource_kind == "custom-copilot":
        # Copy from customizations directory (formerly "reference")
        source_rel = resource.get("source")
        customizations_path = get_customizations_path()
        source_path = customizations_path / source_rel
        
        if not source_path.exists():
            print(f"Warning: Referenced resource not found: {source_path}")
            return False
        
        if source_path.is_dir():
            dest_path = dest_dir / resource_name
            if dest_path.exists():
                shutil.rmtree(dest_path)
            shutil.copytree(source_path, dest_path)
        else:
            dest_path = dest_dir / source_path.name
            shutil.copy2(source_path, dest_path)
        
        print(f"  ✓ Installed {resource_type[:-1]} '{resource_name}' from custom-copilot")
        return True
    
    elif resource_kind == "custom":
        # Copy from a custom git source repository
        source_name = resource.get("source_name")
        source_rel = resource.get("source")
        
        if not source_name:
            print(f"Error: 'custom' type requires 'source_name' field")
            return False
        
        if not source_rel:
            print(f"Error: 'custom' type requires 'source' field")
            return False
        
        # Get the custom source path (clones/updates repo if needed)
        custom_source_path = get_custom_source_path(source_name)
        if not custom_source_path:
            print(f"Warning: Could not access custom source '{source_name}'")
            return False
        
        source_path = custom_source_path / source_rel
        
        if not source_path.exists():
            print(f"Warning: Custom resource not found: {source_path}")
            return False
        
        if source_path.is_dir():
            dest_path = dest_dir / resource_name
            if dest_path.exists():
                shutil.rmtree(dest_path)
            shutil.copytree(source_path, dest_path)
        else:
            dest_path = dest_dir / source_path.name
            shutil.copy2(source_path, dest_path)
        
        print(f"  ✓ Installed {resource_type[:-1]} '{resource_name}' from custom source '{source_name}'")
        return True
    
    elif resource_kind == "github":
        # Support for direct GitHub URLs
        github_url = resource.get("url")
        
        if not github_url:
            print(f"Error: 'github' type requires 'url' field")
            return False
        
        # Import here to avoid circular dependency
        from custom_copilot.config import parse_github_url, download_github_file, clone_or_update_repo
        
        github_info = parse_github_url(github_url)
        if not github_info:
            print(f"Error: Invalid GitHub URL: {github_url}")
            return False
        
        owner = github_info["owner"]
        repo = github_info["repo"]
        path = github_info["path"]
        ref = github_info["ref"]
        
        # For file URLs
        if path and (path.endswith(".md") or "." in Path(path).name):
            print(f"  Downloading {resource_name} from GitHub...")
            temp_file = download_github_file(owner, repo, path, ref)
            
            if not temp_file:
                print(f"  ⚠ Failed to download from GitHub: {github_url}")
                return False
            
            # Determine destination
            file_name = Path(path).name
            dest_path = dest_dir / file_name
            shutil.copy2(temp_file, dest_path)
            temp_file.unlink()
            
            print(f"  ✓ Installed {resource_type[:-1]} '{resource_name}' from GitHub")
            return True
        else:
            # For folder/repo URLs - clone and copy
            print(f"  Cloning {owner}/{repo} from GitHub...")
            temp_source = {
                "name": f"{owner}_{repo}_bundle",
                "type": "git",
                "url": f"https://github.com/{owner}/{repo}.git"
            }
            
            repo_path = clone_or_update_repo(temp_source)
            if not repo_path:
                print(f"  ⚠ Failed to clone from GitHub: {github_url}")
                return False
            
            # Determine source path
            source_path = repo_path / path if path else repo_path
            
            if not source_path.exists():
                print(f"  ⚠ Path not found in repository: {path}")
                return False
            
            # Copy to destination
            if source_path.is_dir():
                dest_path = dest_dir / resource_name
                if dest_path.exists():
                    shutil.rmtree(dest_path)
                shutil.copytree(source_path, dest_path)
            else:
                dest_path = dest_dir / source_path.name
                shutil.copy2(source_path, dest_path)
            
            print(f"  ✓ Installed {resource_type[:-1]} '{resource_name}' from GitHub")
            return True
    
    elif resource_kind == "agentskills":
        # Support for agentskills.io repositories
        # Format: { "type": "agentskills", "repo": "owner/repo", "skill": "skill-name" }
        repo_ref = resource.get("repo", "anthropics/skills")  # Default to anthropics/skills
        skill_name = resource.get("skill") or resource_name
        
        print(f"  Installing skill '{skill_name}' from agentskills repo '{repo_ref}'...")
        
        # Parse repo reference
        if "/" in repo_ref:
            owner, repo = repo_ref.split("/", 1)
        else:
            owner, repo = "anthropics", repo_ref
        
        # Clone the repository
        from custom_copilot.config import clone_or_update_repo
        temp_source = {
            "name": f"agentskills_{owner}_{repo}",
            "type": "git",
            "url": f"https://github.com/{owner}/{repo}.git"
        }
        
        repo_path = clone_or_update_repo(temp_source)
        if not repo_path:
            print(f"  ⚠ Failed to clone agentskills repository")
            return False
        
        # Look for the skill in skills/ folder
        skill_path = repo_path / "skills" / skill_name
        if not skill_path.exists() or not (skill_path / "SKILL.md").exists():
            print(f"  ⚠ Skill '{skill_name}' not found in repository")
            return False
        
        # Copy the skill folder
        dest_path = dest_dir / skill_name
        if dest_path.exists():
            shutil.rmtree(dest_path)
        shutil.copytree(skill_path, dest_path)
        
        print(f"  ✓ Installed skill '{skill_name}' from agentskills repository")
        return True
    
    # Support legacy "inline" and "reference" types for backward compatibility
    elif resource_kind == "inline":
        print(f"  ⚠ Warning: 'inline' type is deprecated, use 'bundle' instead")
        resource["type"] = "bundle"
        return install_bundle_resource(bundle_path, resource_type, resource, dest_dir)
    
    elif resource_kind == "reference":
        print(f"  ⚠ Warning: 'reference' type is deprecated, use 'custom-copilot' instead")
        resource["type"] = "custom-copilot"
        return install_bundle_resource(bundle_path, resource_type, resource, dest_dir)
    
    return False


def install_bundle(bundle_name: str) -> bool:
    """
    Install a bundle to the project's .github directory.
    
    Args:
        bundle_name: Name of the bundle to install
        
    Returns:
        True if successful, False otherwise
    """
    # Load bundle manifest
    manifest = load_bundle_manifest(bundle_name)
    if not manifest:
        print(f"Error: Bundle '{bundle_name}' not found or invalid manifest")
        print(f"\nAvailable bundles:")
        for bundle in list_available_bundles():
            print(f"  - {bundle}")
        return False
    
    print(f"Installing bundle: {manifest.get('name')} v{manifest.get('version')}")
    print(f"Description: {manifest.get('description', 'No description')}")
    print()
    
    bundle_path = get_customizations_path() / "bundles" / bundle_name
    github_dir = get_github_dir()
    
    # Check if .github exists
    if not github_dir.exists():
        print("Error: .github directory not found")
        print("Run 'cuco init' first to initialize the structure")
        return False
    
    # Install copilot instructions if specified
    copilot_instr = manifest.get("copilotInstructions")
    if copilot_instr and copilot_instr.get("type") == "inline":
        instr_path = bundle_path / copilot_instr.get("path")
        if instr_path.exists():
            dest_path = github_dir / "copilot-instructions.md"
            
            # Ask for confirmation if file exists
            if dest_path.exists():
                response = input(f"copilot-instructions.md already exists. Overwrite? [y/N]: ")
                if response.lower() != 'y':
                    print("Skipping copilot-instructions.md")
                else:
                    shutil.copy2(instr_path, dest_path)
                    print(f"✓ Installed copilot-instructions.md")
            else:
                shutil.copy2(instr_path, dest_path)
                print(f"✓ Installed copilot-instructions.md")
    
    # Install dependencies
    dependencies = manifest.get("dependencies", {})
    
    # Install agents
    agents = dependencies.get("agents", [])
    if agents:
        print(f"\nInstalling {len(agents)} agent(s)...")
        agents_dir = github_dir / "agents"
        agents_dir.mkdir(exist_ok=True)
        for agent in agents:
            install_bundle_resource(bundle_path, "agents", agent, agents_dir)
    
    # Install prompts
    prompts = dependencies.get("prompts", [])
    if prompts:
        print(f"\nInstalling {len(prompts)} prompt(s)...")
        prompts_dir = github_dir / "prompts"
        prompts_dir.mkdir(exist_ok=True)
        for prompt in prompts:
            install_bundle_resource(bundle_path, "prompts", prompt, prompts_dir)
    
    # Install skills
    skills = dependencies.get("skills", [])
    if skills:
        print(f"\nInstalling {len(skills)} skill(s)...")
        skills_dir = github_dir / "skills"
        skills_dir.mkdir(exist_ok=True)
        for skill in skills:
            install_bundle_resource(bundle_path, "skills", skill, skills_dir)
    
    # Install instructions
    instructions = dependencies.get("instructions", [])
    if instructions:
        print(f"\nInstalling {len(instructions)} instruction(s)...")
        instructions_dir = github_dir / "instructions"
        instructions_dir.mkdir(exist_ok=True)
        for instruction in instructions:
            install_bundle_resource(bundle_path, "instructions", instruction, instructions_dir)
    
    print(f"\n✓ Bundle '{bundle_name}' installed successfully!")
    return True


def run(args: List[str]) -> int:
    """
    Run the bundle command.
    
    Args:
        args: Command arguments
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    if len(args) < 1:
        print("Error: Missing bundle operation")
        print("Usage: cuco bundle <operation> [args]")
        print("Operations: list, add")
        return 1
    
    operation = args[0]
    
    if operation == "list":
        bundles = list_available_bundles()
        if not bundles:
            print("No bundles available")
            return 0
        
        print("Available bundles:")
        for bundle_name in bundles:
            manifest = load_bundle_manifest(bundle_name)
            if manifest:
                version = manifest.get("version", "unknown")
                description = manifest.get("description", "No description")
                print(f"  - {bundle_name} (v{version})")
                print(f"    {description}")
        return 0
    
    elif operation == "add":
        if len(args) < 2:
            print("Error: Missing bundle name")
            print("Usage: cuco bundle add <bundle-name>")
            return 1
        
        bundle_name = args[1]
        if install_bundle(bundle_name):
            return 0
        else:
            return 1
    
    else:
        print(f"Error: Unknown bundle operation '{operation}'")
        print("Valid operations: list, add")
        return 1
