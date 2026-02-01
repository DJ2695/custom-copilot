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
        print("\nExamples:")
        print("  cuco source add my-company https://github.com/mycompany/copilot-customs.git")
        print("  cuco source list")
        print("  cuco source remove my-company")
        return 1
    
    operation = args[0]
    
    if operation == "list":
        sources = get_custom_sources()
        if not sources:
            print("No custom sources configured")
            print(f"\nConfiguration file: {get_config_path()}")
            print("\nAdd a git source with: cuco source add <name> <url>")
            print("\nExamples:")
            print("  cuco source add my-company https://github.com/mycompany/copilot-customs.git")
            print("  cuco source add my-company git@github.com:mycompany/copilot-customs.git")
            return 0
        
        print("Configured git sources:")
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
        if len(args) < 3:
            print("Error: Missing arguments")
            print("Usage: cuco source add <name> <url>")
            print("\nExamples:")
            print("  # HTTPS (requires git credentials or token)")
            print("  cuco source add my-company https://github.com/mycompany/copilot-customs.git")
            print("")
            print("  # SSH (requires SSH key setup)")
            print("  cuco source add my-company git@github.com:mycompany/copilot-customs.git")
            print("")
            print("Note: The repository must contain a 'custom_copilot' folder with your customizations")
            return 1
        
        name = args[1]
        url = args[2]
        
        # Validate URL is a git repository
        if not (url.endswith('.git') or url.startswith('git@') or 'github.com' in url or 'gitlab.com' in url):
            print("Warning: URL does not appear to be a git repository")
            print("Continuing anyway...")
        
        if add_custom_source(name, "git", url):
            print(f"✓ Added git source '{name}'")
            print(f"  URL: {url}")
            print(f"\nConfiguration saved to: {get_config_path()}")
            print(f"\nYou can now reference resources from this source using:")
            print(f"  \"type\": \"custom\",")
            print(f"  \"source_name\": \"{name}\",")
            print(f"  \"source\": \"agents/my-agent.agent.md\"")
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
