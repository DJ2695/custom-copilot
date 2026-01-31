---
name: github-copilot-customizer
description: 'Comprehensive guide for customizing GitHub Copilot through workspace instructions, custom agents, prompts, and conditional instruction files. Use when: creating copilot-instructions.md, setting up custom agents, building reusable prompts, configuring file-specific instructions, organizing .github/copilot folder structure, or any GitHub Copilot customization task. Triggers on: "customize copilot", "copilot instructions", "create agent", "prompt file", "instruction file", ".github setup".'
---

# GitHub Copilot Customizer

Guide for tailoring GitHub Copilot to your project's specific needs through five customization methods: workspace instructions, custom agents, prompts, conditional instruction files, and skills.

## When to Use This Skill

- Creating or updating `.github/copilot-instructions.md`
- Building custom agents in `.github/agents/`
- Creating reusable prompt files in `.github/prompts/`
- Setting up file-type-specific instruction files in `.github/instructions/`
- Organizing GitHub Copilot customization folder structure
- Configuring MCP servers in `.github/mcp.json`
- Understanding which customization method fits your use case

## Prerequisites

- VS Code with GitHub Copilot extension
- Enable instruction files in `.vscode/settings.json`:
```json
{
  "github.copilot.chat.codeGeneration.useInstructionFiles": true
}
```

## Customization Methods Overview

| Method | Location | Purpose | Scope |
|--------|----------|---------|-------|
| **Workspace Instructions** | `.github/copilot-instructions.md` | Baseline project-wide rules | All chat requests |
| **Agents** | `.github/agents/*.md` | Specialized task workflows | On-demand via @agent |
| **Prompts** | `.github/prompts/*.md` | Reusable task templates | On-demand invocation |
| **Instruction Files** | `.github/instructions/*.instructions.md` | Conditional file-type rules | Auto-applied by glob |
| **Skills** | `.github/skills/*/SKILL.md` | Domain knowledge packages | Agent-loaded as needed |

## Recommended Directory Structure

```
.github/
├── copilot-instructions.md
├── agents/
│   ├── planner.md
│   ├── implementer.md
│   └── reviewer.md
├── prompts/
│   ├── generate-component.md
│   └── security-review.md
├── instructions/
│   ├── general-coding.instructions.md
│   ├── python-coding.instructions.md
│   └── typescript-coding.instructions.md
├── skills/
│   └── [domain-skill]/SKILL.md
└── mcp.json
```

---

## 1. Workspace Instructions

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

---

## 2. Custom Agents

**Location**: `.github/agents/[agent-name].md`

Specialized AI agents for specific development workflows with custom tools and handoffs.

### Template

```markdown
---
description: [Brief purpose - shown in UI]
name: [Display Name]
tools: ['search', 'fetch', 'githubRepo', 'usages']
model: Claude Sonnet 4.5.5
handoffs:
  - label: [Button text]
    agent: [target-agent]
    prompt: [Optional handoff prompt]
    send: false
---

# [Agent Name] Instructions

[Core behavior and purpose]

## Task Guidelines
- [Specific requirements]
- [Output format]

## Process
1. [Step 1]
2. [Step 2]
```

### Available Tools

| Tool | Purpose |
|------|---------|
| `search` | Search codebase |
| `fetch` | Fetch web content |
| `githubRepo` | Access GitHub repository data |
| `usages` | Find code usages |
| `search/codebase` | Detailed codebase search |

### Available Models

- `Claude Sonnet 4.5.5` (recommended for planning and research)
- `Claude Opus 4.5` (recommended for implementation)
- `Claude Haiku 4.5` (recommended for fast / easy tasks)
- Default (omit `model` field)

### Common Agent Patterns

**Planner Agent** - Generates implementation plans without code edits:
```markdown
---
description: Generate implementation plans for features
name: Planner
tools: ['search', 'githubRepo']
model: Claude Sonnet 4.5
handoffs:
  - label: Implement Plan
    agent: agent
    send: false
---

You are in planning mode. Generate comprehensive plans without code edits.

## Plan Structure
1. Overview
2. Requirements
3. Implementation steps
4. Testing strategy
```

**Reviewer Agent** - Code review and quality checks:
```markdown
---
description: Review code for quality and best practices
name: Reviewer
tools: ['search', 'usages']
model: Claude Sonnet 4.5
---

Review code against project standards. Check for:
- Code quality issues
- Security concerns
- Performance problems
- Test coverage gaps
```

---

## 3. Prompt Files

**Location**: `.github/prompts/[task-name].md`

Reusable, task-specific prompts invoked on-demand.

### Template

```markdown
---
agent: 'agent'
model: Claude Sonnet 4.5
tools: ['githubRepo', 'search/codebase']
description: 'Brief description for UI'
---

# [Task Name]

[Task instructions]

## Context
Reference templates: #tool:githubRepo org/repo-templates
Reference local: [design-system.md](../docs/design-system.md)

## Requirements
- [Requirement 1]
- [Requirement 2]

## Output Format
- [Expected format]
```

### Agent Types

| Type | Use For |
|------|---------|
| `agent` | Code generation tasks |
| `ask` | Analysis, review, non-coding tasks |

### Tool References

```markdown
# GitHub repository
#tool:githubRepo contoso/templates

# Local files (relative path)
[design.md](../docs/design.md)

# Tools
#tool:search/codebase
#tool:fetch
```

### Example: Component Generator

```markdown
---
agent: 'agent'
tools: ['githubRepo', 'search/codebase']
description: 'Generate React component from design system'
---

# React Component Generator

Generate component using #tool:githubRepo org/design-system.

## Initial Questions
Ask for component name and purpose if not provided.

## Requirements
- Use TypeScript with explicit prop types
- Follow design system patterns
- Include unit tests
- Add Storybook story
```

---

## 4. Instruction Files

**Location**: `.github/instructions/[topic].instructions.md`

Conditional, file-type-specific guidelines auto-applied based on glob patterns.

### Template

```markdown
---
applyTo: "**/*.py"
---

# [Language/Topic] Guidelines

[Guidelines that apply when glob matches]

## Standards
- [Standard 1]
- [Standard 2]

## Patterns
- [Pattern 1]
- [Pattern 2]
```

### Glob Pattern Examples

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

**General** (`general-coding.instructions.md`):
```markdown
---
applyTo: "**"
---
# General Coding Standards
- Use meaningful names
- Keep functions focused
- Handle errors properly
```

**Language-specific** (`python-coding.instructions.md`):
```markdown
---
applyTo: "**/*.py"
---
Apply [general guidelines](./general-coding.instructions.md).

# Python Standards
- Follow PEP 8
- Use type hints
- Write docstrings (Google format)
```

**Framework-specific** (`django-coding.instructions.md`):
```markdown
---
applyTo: "apps/**/*.py"
---
Apply [Python guidelines](./python-coding.instructions.md).

# Django Standards
- Use class-based views
- Follow fat models pattern
```

---

## 5. Skills

**Location**: `.github/skills/[skill-name]/SKILL.md`

Skills are modular knowledge packages for specialized domains. For detailed guidance on creating skills, use the **skill-creator** skill which provides comprehensive instructions on skill structure, bundled resources, and best practices.

### Quick Overview

Skills provide:
- Domain expertise (schemas, business logic)
- Specialized workflows
- Bundled resources (scripts, references, templates)

### Basic Structure

```
skill-name/
├── SKILL.md              # Required
├── references/           # Documentation
├── scripts/              # Executable code
├── assets/               # Static files
└── templates/            # Code scaffolds
```

### Integration with Other Methods

Reference skills from other customization files:
- In agents: Point to skill documentation
- In prompts: Create prompts that leverage skill knowledge
- In instructions: Reference skill files for detailed guidance

---

## MCP Server Configuration

**File**: `.github/mcp.json`

Extend Copilot with additional tools via Model Context Protocol.

### Template

```json
{
  "servers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@org/server-package"]
    },
    "http-server": {
      "type": "http",
      "url": "https://example.com/mcp"
    }
  },
  "inputs": [
    {
      "type": "promptString",
      "id": "api-key",
      "description": "API Key",
      "password": true
    }
  ]
}
```

---

## VS Code Settings

Configure in `.vscode/settings.json`:

```json
{
  "github.copilot.chat.codeGeneration.useInstructionFiles": true,
  
  "github.copilot.chat.pullRequestDescriptionGeneration.instructions": [
    { "text": "Include list of key changes." },
    { "text": "Reference related issues." }
  ],
  
  "github.copilot.chat.reviewSelection.instructions": [
    { "file": ".github/instructions/code-review.instructions.md" }
  ]
}
```

---

## Decision Guide: Which Method to Use

| Scenario | Method |
|----------|--------|
| Project-wide coding standards | `copilot-instructions.md` |
| Multi-step workflow with handoffs | Custom Agent |
| Reusable task template | Prompt File |
| Rules for specific file types | Instruction File |
| Deep domain knowledge | Skill |
| External tool integration | MCP Server |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Instructions not applied | Verify `useInstructionFiles` is `true` in settings |
| Agent not visible | Check YAML frontmatter syntax, ensure `.md` extension |
| Glob not matching | Test pattern, ensure correct syntax |
| Tool reference fails | Verify tool in agent's `tools` list |
| Conflicting rules | Order files general → specific, use explicit references |

## References

- [VS Code Copilot Customization](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
- [Custom Agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- [Prompt Files](https://code.visualstudio.com/docs/copilot/customization/prompt-files)
- [MCP Servers](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
