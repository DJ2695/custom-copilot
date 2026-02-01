"""
Bundle command - Manage copilot customization bundles.

This module implements bundle operations including listing, adding, and
managing bundles which are pre-configured combinations of copilot customizations.
"""

import json
import shutil
from pathlib import Path
from typing import List, Dict, Optional
from cc.utils import (
    get_github_dir,
    track_artifact,
    calculate_file_hash,
    calculate_dir_hash
)


def get_customizations_path() -> Path:
    """
    Get the path to the copilot-customizations directory.
    
    Returns:
        Path to copilot-customizations directory in the package
    """
    package_dir = Path(__file__).parent.parent
    return package_dir.parent.parent / "copilot-customizations"


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
    Install a bundle resource (inline or reference).
    
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
    
    if resource_kind == "inline":
        # Copy from bundle directory
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
        
        print(f"  ✓ Installed inline {resource_type[:-1]} '{resource_name}'")
        return True
        
    elif resource_kind == "reference":
        # Copy from customizations directory
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
        
        version = resource.get("version", "unknown")
        print(f"  ✓ Installed {resource_type[:-1]} '{resource_name}' (version: {version})")
        return True
    
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
