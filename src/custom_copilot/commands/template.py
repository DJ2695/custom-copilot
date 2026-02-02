"""
Template command - Create new resources from templates.

This module implements the `cuco template` command which helps create
new agents, skills, prompts, instructions, bundles, and MCP servers from templates.
"""

import shutil
from pathlib import Path
from typing import List
from custom_copilot.utils import get_registry_path, get_target_dir


def create_from_template(resource_type: str, name: str, output_path: Path = None) -> bool:
    """
    Create a new resource from a template.
    
    Args:
        resource_type: Type of resource (agent, skill, prompt, instructions, bundle, mcp)
        name: Name for the new resource
        output_path: Optional output path (defaults to current target directory)
        
    Returns:
        True if successful, False otherwise
    """
    # Get the templates directory - it's at the repo root level
    registry_path = get_registry_path()
    # Go up to package root, then to custom_copilot/templates
    package_root = registry_path.parent.parent.parent  # Go up from registry/ to package root
    templates_dir = package_root / "custom_copilot" / "templates"
    
    # Map resource types to templates
    template_map = {
        "agent": "agent-template.agent.md",
        "prompt": "prompt-template.prompt.md",
        "skill": "skill-template",
        "bundle": "bundle-template"
    }
    
    if resource_type not in template_map:
        print(f"Error: Unknown resource type '{resource_type}'")
        print(f"Available types: {', '.join(template_map.keys())}")
        return False
    
    template_name = template_map[resource_type]
    template_path = templates_dir / template_name
    
    if not template_path.exists():
        print(f"Error: Template '{template_name}' not found at {template_path}")
        return False
    
    # Determine output location
    if output_path is None:
        target_dir = get_target_dir()
        
        if resource_type == "agent":
            output_path = target_dir / "agents" / f"{name}.agent.md"
        elif resource_type == "prompt":
            output_path = target_dir / "prompts" / f"{name}.prompt.md"
        elif resource_type == "skill":
            output_path = target_dir / "skills" / name
        elif resource_type == "bundle":
            output_path = target_dir / "bundles" / name
    
    # Check if already exists
    if output_path.exists():
        response = input(f"'{output_path}' already exists. Overwrite? [y/N]: ")
        if response.lower() != 'y':
            print("Cancelled.")
            return False
    
    # Create from template
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if template_path.is_file():
            # Copy file template
            shutil.copy2(template_path, output_path)
            
            # Replace placeholders
            content = output_path.read_text()
            content = content.replace("{{NAME}}", name)
            content = content.replace("{{name}}", name)
            output_path.write_text(content)
            
            print(f"✓ Created {resource_type} template at {output_path}")
        else:
            # Copy directory template
            shutil.copytree(template_path, output_path, dirs_exist_ok=True)
            
            # Replace placeholders in all files
            for file_path in output_path.rglob("*"):
                if file_path.is_file() and file_path.suffix in [".md", ".json"]:
                    try:
                        content = file_path.read_text()
                        content = content.replace("{{NAME}}", name)
                        content = content.replace("{{name}}", name)
                        file_path.write_text(content)
                    except Exception:
                        pass  # Skip binary files
            
            print(f"✓ Created {resource_type} template at {output_path}")
        
        print(f"\nNext steps:")
        print(f"  1. Edit the template files in {output_path}")
        print(f"  2. Customize the content for your use case")
        if resource_type in ["agent", "skill", "prompt"]:
            print(f"  3. Test with GitHub Copilot")
        
        return True
        
    except Exception as e:
        print(f"Error creating template: {e}")
        return False


def list_templates() -> None:
    """List available templates."""
    print("Available templates:")
    print("  agent       - Custom agent template (.agent.md)")
    print("  prompt      - Reusable prompt template (.prompt.md)")
    print("  skill       - Skill template (folder with SKILL.md)")
    print("  bundle      - Bundle template with manifest")


def run(args: List[str]) -> int:
    """
    Run the template command.
    
    Args:
        args: Command arguments [create|list] [type] [name] [--output=path]
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    if len(args) == 0 or args[0] in ["help", "--help", "-h"]:
        print("Usage: cuco template <command> [options]")
        print("\nCommands:")
        print("  create <type> <name>  - Create a new resource from template")
        print("  list                  - List available templates")
        print("\nTypes:")
        print("  agent, prompt, skill, bundle")
        print("\nOptions:")
        print("  --output=<path>       - Specify output path")
        print("\nExamples:")
        print("  cuco template create agent my-agent")
        print("  cuco template create skill my-skill")
        print("  cuco template list")
        return 0
    
    command = args[0]
    
    if command == "list":
        list_templates()
        return 0
    
    elif command == "create":
        if len(args) < 3:
            print("Error: Missing arguments")
            print("Usage: cuco template create <type> <name> [--output=path]")
            return 1
        
        resource_type = args[1]
        name = args[2]
        output_path = None
        
        # Parse output path if provided
        for arg in args[3:]:
            if arg.startswith("--output="):
                output_path = Path(arg.split("=", 1)[1])
        
        if create_from_template(resource_type, name, output_path):
            return 0
        else:
            return 1
    
    else:
        print(f"Error: Unknown command '{command}'")
        print("Run 'cuco template help' for usage information.")
        return 1
