"""
Source command - Manage custom copilot customization sources.

This module implements source management for adding/removing custom
repositories (e.g., private company repos) as sources for bundles and customizations.
"""

from typing import List
from custom_copilot.config import (
    get_custom_sources,
    add_custom_source,
    remove_custom_source,
    get_config_path
)


def run(args: List[str]) -> int:
    """
    Run the source command.
    
    Args:
        args: Command arguments
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    if len(args) < 1:
        print("Error: Missing source operation")
        print("Usage: cuco source <operation> [args]")
        print("Operations: list, add, remove")
        return 1
    
    operation = args[0]
    
    if operation == "list":
        sources = get_custom_sources()
        if not sources:
            print("No custom sources configured")
            print(f"\nConfiguration file: {get_config_path()}")
            print("\nAdd a source with: cuco source add <name> <type> <url>")
            return 0
        
        print("Configured custom sources:")
        for source in sources:
            name = source.get("name", "unknown")
            source_type = source.get("type", "unknown")
            url = source.get("url", "unknown")
            print(f"  - {name}")
            print(f"    Type: {source_type}")
            print(f"    URL: {url}")
        
        print(f"\nConfiguration file: {get_config_path()}")
        return 0
    
    elif operation == "add":
        if len(args) < 4:
            print("Error: Missing arguments")
            print("Usage: cuco source add <name> <type> <url>")
            print("\nExamples:")
            print("  cuco source add company-internal git https://github.com/mycompany/copilot-customs.git")
            print("  cuco source add local-dev local /path/to/local/customizations")
            return 1
        
        name = args[1]
        source_type = args[2]
        url = args[3]
        
        if add_custom_source(name, source_type, url):
            print(f"✓ Added custom source '{name}'")
            print(f"  Type: {source_type}")
            print(f"  URL: {url}")
            print(f"\nConfiguration saved to: {get_config_path()}")
            return 0
        else:
            print(f"Error: Failed to add source '{name}'")
            return 1
    
    elif operation == "remove":
        if len(args) < 2:
            print("Error: Missing source name")
            print("Usage: cuco source remove <name>")
            return 1
        
        name = args[1]
        if remove_custom_source(name):
            print(f"✓ Removed custom source '{name}'")
            return 0
        else:
            print(f"Error: Source '{name}' not found")
            return 1
    
    else:
        print(f"Error: Unknown source operation '{operation}'")
        print("Valid operations: list, add, remove")
        return 1
