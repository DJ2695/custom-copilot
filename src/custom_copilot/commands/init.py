"""
Init command - Initialize folder structure for agent customizations.

This module implements the `cuco init` command which creates the standard
folder structure for agent customizations based on the chosen integration engine.
"""

from pathlib import Path
from typing import List


INTEGRATION_ENGINES = {
    "github": {
        "folder": ".github",
        "subdirs": ["agents", "prompts", "instructions", "skills"],
        "main_file": "copilot-instructions.md",
        "description": "GitHub Copilot (default)"
    },
    "claude": {
        "folder": ".claude",
        "subdirs": ["agents", "prompts", "skills"],
        "main_file": "instructions.md",
        "description": "Claude Code"
    },
    "cuco": {
        "folder": ".cuco",
        "subdirs": ["agents", "prompts", "instructions", "skills", "bundles", "mcps"],
        "main_file": "config.json",
        "description": "Tool-agnostic CUCO format"
    }
}


def run(args: List[str]) -> int:
    """
    Run the init command.
    
    Creates folder structure based on the chosen integration engine:
    - .github/ for GitHub Copilot (default)
    - .claude/ for Claude Code
    - .cuco/ for tool-agnostic format
    
    Args:
        args: Command arguments [--engine=<name>]
        
    Returns:
        Exit code (0 for success)
    """
    # Parse arguments
    engine = "github"  # Default
    for arg in args:
        if arg.startswith("--engine="):
            engine = arg.split("=", 1)[1]
        elif arg in ["--help", "-h"]:
            print("Usage: cuco init [--engine=<name>]")
            print("\nAvailable engines:")
            for key, info in INTEGRATION_ENGINES.items():
                print(f"  {key:10} - {info['description']}")
            return 0
    
    if engine not in INTEGRATION_ENGINES:
        print(f"Error: Unknown engine '{engine}'")
        print(f"Available engines: {', '.join(INTEGRATION_ENGINES.keys())}")
        return 1
    
    config = INTEGRATION_ENGINES[engine]
    print(f"Initializing {config['folder']} folder structure ({config['description']})...")
    
    # Get project root (current directory)
    project_root = Path.cwd()
    target_dir = project_root / config["folder"]
    
    # Create main directory
    target_dir.mkdir(exist_ok=True)
    print(f"✓ Created {target_dir.relative_to(project_root)}/")
    
    # Create subdirectories
    for subdir in config["subdirs"]:
        subdir_path = target_dir / subdir
        subdir_path.mkdir(exist_ok=True)
        print(f"✓ Created {subdir_path.relative_to(project_root)}/")
    
    # Create main configuration file if it doesn't exist
    main_file = target_dir / config["main_file"]
    if not main_file.exists():
        if config["main_file"] == "config.json":
            # Create initial config.json for .cuco
            import json
            initial_config = {
                "version": "1.0.0",
                "sources": [],
                "integrations": {
                    "github": False,
                    "claude": False
                }
            }
            with open(main_file, 'w') as f:
                json.dump(initial_config, f, indent=2)
        else:
            main_file.touch()
        print(f"✓ Created {main_file.relative_to(project_root)}")
    else:
        print(f"  {main_file.relative_to(project_root)} already exists")
    
    print("\n✓ Initialization complete!")
    print("\nYou can now add resources using:")
    print("  cuco add agent <name>")
    print("  cuco add prompt <name>")
    print("  cuco add skill <name>")
    if engine == "github":
        print("  cuco add instructions <name>")
    
    return 0
