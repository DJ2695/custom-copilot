# Example Bundle Copilot Instructions

This bundle demonstrates how to combine copilot customizations effectively.

## Available Agents

### skill-builder
Use the skill-builder agent when you need to create or modify GitHub Copilot skills. This agent has specialized knowledge about skill structure and best practices.

**When to use:**
- Creating new skills
- Modifying existing skills
- Validating skill structure

**Example:**
```
@skill-builder create a new skill for Python testing with pytest
```

## Available Skills

### test-driven-development
This skill enforces the RED-GREEN-REFACTOR TDD cycle. Use it when implementing any feature or bugfix.

**Workflow:**
1. Write a failing test first (RED)
2. Write minimal code to pass the test (GREEN)
3. Refactor while keeping tests green (REFACTOR)

## Available Prompts

### git
Use for Git operations and repository management.

### custom-prompt
A bundle-specific prompt demonstrating inline resources that are only relevant when using this bundle.

## Working with This Bundle

When this bundle is installed:
1. The copilot-instructions.md explains how components work together
2. All referenced agents, skills, and prompts are automatically available
3. Bundle-specific resources (like custom-prompt) are included inline
4. All dependencies are resolved and validated

## Dependencies

This bundle ensures all required resources are available:
- ✓ skill-builder agent (from central registry)
- ✓ test-driven-development skill (from central registry)
- ✓ git prompt (from central registry)
- ✓ custom-prompt (inline in bundle)
