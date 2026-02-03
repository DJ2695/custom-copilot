"""
Command-line interface for custom-copilot.

This module provides the main CLI entry point and command routing.
"""

import sys
from typing import List, Optional
from custom_copilot.commands import init, add, sync, list as list_cmd, bundle, source, template, publish


def print_help():
    """Print CLI help message."""
    help_text = """
Custom Copilot CLI (cuco) - Fast Customization of Agentic Coding Agents

Usage:
    cuco init [--engine=<name>]                Initialize folder structure
    cuco add agent <name>                      Add an agent from registry
    cuco add prompt <name>                     Add a prompt from registry
    cuco add instructions <name>               Add instructions from registry
    cuco add skill <name>                      Add a skill from registry
    cuco add mcp <name>                        Add an MCP server from registry
    cuco template create <type> <name>         Create resource from template
    cuco template list                         List available templates
    cuco publish <path> [options]              Publish resource to destination
    cuco bundle list                           List available bundles
    cuco bundle add <name>                     Install a bundle
    cuco source list                           List configured git sources
    cuco source add <name> <url>               Add a git source repository
    cuco source remove <name>                  Remove a git source
    cuco list <type>                           List available artifacts in registry
    cuco sync                                  Sync all artifacts from registry
    cuco sync <artifact-name>                  Sync specific artifact from registry
    cuco help                                  Show this help message

Integration Engines (for init):
    github     - GitHub Copilot (default) - creates .github/ folder
    claude     - Claude Code - creates .claude/ folder
    cuco       - Tool-agnostic format - creates .cuco/ folder

Examples:
    # Initialize project
    cuco init
    cuco init --engine=claude
    
    # Add resources
    cuco add agent skill-builder
    cuco add skill test-driven-development
    
    # Create from templates
    cuco template create agent my-agent
    cuco template create skill my-skill
    
    # Publish resources
    cuco publish ./my-skill --type=skill --source=marketplace
    cuco publish ./my-agent.agent.md --source=git-commit --destination=/path/to/repo/agents
    
    # Use bundles
    cuco bundle add development-essentials
    
    # Add skills from GitHub URLs
    cuco add skill https://github.com/anthropics/skills/tree/main/skills/brand-guidelines
    cuco add skill https://github.com/owner/repo/blob/main/path/to/skill
    
    # Add a private git repository
    cuco source add my-company https://github.com/mycompany/copilot-customs.git
    cuco source list

Resource Types:
    agent, prompt, skill, instructions, bundle, mcp

Supported Standards:
    - AgentSkills.io (anthropics/skills and compatible repos)
    - GitHub Copilot (.github/ folder structure)
    - Claude Code (.claude/ folder structure)
    - MCP (Model Context Protocol servers)
    - Tool-agnostic (.cuco/ folder structure)

Supported Repository Structures for Custom Sources:
    - custom_copilot/  (traditional cuco structure)
    - .cuco/           (alternative cuco structure)
    - .github/         (GitHub Copilot standard)
    - .claude/         (Claude Code standard)
    - skills/          (agentskills.io standard with SKILL.md files)

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
        elif command == "source":
            return source.run(args[1:])
        elif command == "template":
            return template.run(args[1:])
        elif command == "publish":
            return publish.run(args[1:])
        else:
            print(f"Error: Unknown command '{command}'")
            print("Run 'cuco help' for usage information.")
            return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
