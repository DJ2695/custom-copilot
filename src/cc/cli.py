"""
Command-line interface for the cc tool.

This module provides the main CLI entry point and command routing.
"""

import sys
from typing import List, Optional
from cc.commands import init, add, sync, list as list_cmd, bundle


def print_help():
    """Print CLI help message."""
    help_text = """
Custom Copilot CLI (cuco) - Manage GitHub Copilot artifacts

Usage:
    cuco init                                  Initialize .github folder structure
    cuco add agent <name>                      Add an agent from registry
    cuco add prompt <name>                     Add a prompt from registry
    cuco add instructions <name>               Add instructions from registry
    cuco add skill <name>                      Add a skill from registry
    cuco add mcp <name>                        Add an MCP server from registry
    cuco bundle list                           List available bundles
    cuco bundle add <name>                     Install a bundle
    cuco list <type>                           List available artifacts in registry
    cuco sync                                  Sync all artifacts from registry
    cuco sync <artifact-name>                  Sync specific artifact from registry
    cuco help                                  Show this help message

Examples:
    cuco init
    cuco add agent skill-builder
    cuco add skill test-driven-development
    cuco add mcp context7
    cuco bundle list
    cuco bundle add example-bundle
    cuco list skills
    cuco list mcps
    cuco sync
    cuco sync skill-builder

For more information, visit: https://github.com/DJ2695/custom-copilot
"""
    print(help_text)


def main(args: Optional[List[str]] = None) -> int:
    """
    Main CLI entry point.
    
    Args:
        args: Command-line arguments (defaults to sys.argv[1:])
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    if args is None:
        args = sys.argv[1:]
    
    if len(args) == 0 or args[0] in ["help", "--help", "-h"]:
        print_help()
        return 0
    
    command = args[0]
    
    try:
        if command == "init":
            return init.run(args[1:])
        elif command == "add":
            return add.run(args[1:])
        elif command == "sync":
            return sync.run(args[1:])
        elif command == "list":
            return list_cmd.run(args[1:])
        elif command == "bundle":
            return bundle.run(args[1:])
        else:
            print(f"Error: Unknown command '{command}'")
            print("Run 'cuco help' for usage information.")
            return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
