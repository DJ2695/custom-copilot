# Detailed Customization Guide

This file contains detailed information moved from SKILL.md for progressive disclosure.

## Workspace Instructions Details

**File**: `.github/copilot-instructions.md`

Baseline instructions applied to ALL chat requests in the workspace.

### Template

```markdown
# Project Instructions

## Project Overview
- [Framework/stack description]
- [Architectural patterns]

## Coding Standards
- [Naming conventions]
- [Code organization rules]

## Testing Requirements
- [Test framework]
- [Coverage expectations]

## Documentation
- [Doc style requirements]
```

### Best Practices

- Keep concise and actionable
- Focus on project-wide conventions only
- Reference instruction files for detailed guidance
- Avoid implementation-specific details

## Agent Frontmatter Properties

Complete list of all agent frontmatter properties:

| Property | Required | Description |
|----------|----------|-------------|
| `description` | Yes | Brief description shown as placeholder text in chat input field |
| `name` | No | Display name (defaults to filename without .agent.md) |
| `argument-hint` | No | Hint text shown in chat input to guide users |
| `tools` | No | List of tools/tool sets available to this agent |
| `model` | No | AI model to use (defaults to currently selected model) |
| `infer` | No | Enable as subagent (default: true) |
| `target` | No | Target environment: `vscode` or `github-copilot` |
| `mcp-servers` | No | MCP server config JSON (for target: github-copilot) |
| `handoffs` | No | List of suggested next agent transitions |

**Handoff Properties**:
- `label` - Display text on button (prefer emojis: 🚀 ✅ 🔍 📝 🐛 ✏️)
- `agent` - Target agent name (use `name` field or filename without .agent.md)
- `prompt` - Prompt text to send to target agent
- `send` - Auto-submit prompt (default: false)

## Available Models

- `Claude Sonnet 4.5` - Planning and research
- `Claude Opus 4.5` - Implementation and generation
- `Claude Haiku 4.5` - Fast, simple tasks
- Default - Omit `model` field to use current selection

## Prompt File Properties

| Property | Required | Description |
|----------|----------|-------------|
| `agent` | No | Agent type: 'agent' (code gen) or 'ask' (analysis) |
| `model` | No | AI model to use |
| `tools` | No | Tools available to this prompt |
| `description` | No | Brief description for UI |

## Instruction File Glob Patterns

| Pattern | Matches |
|---------|---------|
| `**` | All files |
| `**/*.py` | All Python files |
| `**/*.ts,**/*.tsx` | TypeScript and TSX |
| `src/**/*.ts` | TypeScript in src folder |
| `tests/**/*.test.ts` | Test files |
| `docs/**/*.md` | Documentation files |

### Layered Instructions Pattern

Create a hierarchy from general to specific:

```markdown
# general-coding.instructions.md
---
applyTo: "**"
---
# General Standards
- Use meaningful names
- Keep functions focused

# python-coding.instructions.md
---
applyTo: "**/*.py"
---
Apply [general guidelines](./general-coding.instructions.md).
# Python Standards
- Follow PEP 8
- Use type hints

# django-coding.instructions.md
---
applyTo: "apps/**/*.py"
---
Apply [Python guidelines](./python-coding.instructions.md).
# Django Standards
- Use class-based views
```

## Skills vs Instructions Comparison

| Feature | Agent Skills | Custom Instructions |
|---------|--------------|---------------------|
| **Purpose** | Specialized capabilities + workflows | Coding standards + guidelines |
| **Portability** | Works across VS Code, CLI, cloud | VS Code and GitHub.com only |
| **Content** | Instructions + scripts + resources | Instructions only |
| **Scope** | Task-specific, on-demand | Always applied or glob-based |
| **Standard** | Open (agentskills.io) | VS Code-specific |

## Agent Types for Prompts

| Type | Use For | Example |
|------|---------|---------|
| `agent` | Code generation, file creation, edits | Generate React component |
| `ask` | Analysis, review, explanations | Review code for security |

## Tool Reference Syntax

### In Agent/Prompt Frontmatter
```yaml
tools: ['codebase', 'search', 'edit', 'githubRepo']
```

### In Instructions Body
```markdown
Search using #tool:codebase
Find examples: #tool:githubRepo owner/repo
```

### In Chat
```
#codebase search for authentication
#githubRepo microsoft/vscode extension API
```

## MCP Server Naming Conventions

- Use **camelCase**: `githubIntegration`, `databaseAccess`
- Avoid spaces and special characters
- Use unique, descriptive names
- Reflect functionality or brand

## Using MCP Tools in Agents

```markdown
---
description: Agent using MCP tools
tools: ['serverName/*', 'codebase', 'search']
---
```

- `serverName/*` includes ALL tools from MCP server
- Can also reference individual tool names

## Combining Methods - Advanced Pattern

Effective layering example:

1. **copilot-instructions.md** - "Use clean architecture principles"
2. **python-coding.instructions.md** - "Python files: type hints + docstrings"
3. **planner.agent.md** - References both, uses GitHub MCP tool
4. **generate-api.prompt.md** - Invokes planner with API spec
5. **api-design.skill** - Provides API design patterns

Each layer builds on previous, enabling complex workflows.

## When in Doubt - Default Priority

1. Universal project rule? → `copilot-instructions.md`
2. File-type specific? → Instruction file
3. Repeatable task? → Prompt file
4. Workflow with steps? → Custom agent
5. Deep domain knowledge? → Skill
6. External tool needed? → MCP server
