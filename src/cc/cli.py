"""
Command-line interface for the cc tool.

This module provides the main CLI entry point and command routing.
"""

import sys
from typing import List, Optional
from cc.commands import init, add, sync


def print_help():
    """Print CLI help message."""
    help_text = """
Custom Copilot CLI (cc) - Manage GitHub Copilot artifacts

Usage:
    cc init                                  Initialize .github folder structure
    cc add agent <name>                      Add an agent from registry
    cc add prompt <name>                     Add a prompt from registry
    cc add instructions <name>               Add instructions from registry
    cc add skill <name>                      Add a skill from registry
    cc sync                                  Sync all artifacts from registry
    cc sync <artifact-name>                  Sync specific artifact from registry
    cc help                                  Show this help message

Examples:
    cc init
    cc add agent skill-builder
    cc add skill test-driven-development
    cc sync
    cc sync skill-builder

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
        else:
            print(f"Error: Unknown command '{command}'")
            print("Run 'cc help' for usage information.")
            return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
