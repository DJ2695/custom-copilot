"""
Init command - Initialize .github folder structure.

This module implements the `cc init` command which creates the standard
.github directory structure for GitHub Copilot customizations.
"""

from pathlib import Path
from typing import List


def run(args: List[str]) -> int:
    """
    Run the init command.
    
    Creates the .github folder structure with subdirectories for:
    - agents/
    - prompts/
    - instructions/
    - skills/
    - copilot-instructions.md (empty file)
    
    Args:
        args: Command arguments (unused for init)
        
    Returns:
        Exit code (0 for success)
    """
    print("Initializing .github folder structure...")
    
    # Get project root (current directory)
    project_root = Path.cwd()
    github_dir = project_root / ".github"
    
    # Create main .github directory
    github_dir.mkdir(exist_ok=True)
    print(f"✓ Created {github_dir.relative_to(project_root)}/")
    
    # Create subdirectories
    subdirs = ["agents", "prompts", "instructions", "skills"]
    for subdir in subdirs:
        subdir_path = github_dir / subdir
        subdir_path.mkdir(exist_ok=True)
        print(f"✓ Created {subdir_path.relative_to(project_root)}/")
    
    # Create copilot-instructions.md if it doesn't exist
    instructions_file = github_dir / "copilot-instructions.md"
    if not instructions_file.exists():
        instructions_file.touch()
        print(f"✓ Created {instructions_file.relative_to(project_root)}")
    else:
        print(f"  {instructions_file.relative_to(project_root)} already exists")
    
    print("\n✓ Initialization complete!")
    print("\nYou can now add artifacts using:")
    print("  cc add agent <name>")
    print("  cc add prompt <name>")
    print("  cc add instructions <name>")
    print("  cc add skill <name>")
    
    return 0
