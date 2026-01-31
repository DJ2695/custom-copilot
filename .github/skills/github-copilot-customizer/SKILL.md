---
name: github-copilot-customizer
description: 'Comprehensive guide for customizing GitHub Copilot through workspace instructions, custom agents, prompts, and conditional instruction files. Use when: creating copilot-instructions.md, setting up custom agents, building reusable prompts, configuring file-specific instructions, organizing .github/copilot folder structure, or any GitHub Copilot customization task. Triggers on: "customize copilot", "copilot instructions", "create agent", "prompt file", "instruction file", ".github setup".'
---

# GitHub Copilot Customizer

Tailor GitHub Copilot through six customization methods. This skill provides navigation to detailed guides.

## When to Use This Skill

Use this when you need to:
- Create or modify `.github/copilot-instructions.md`
- Build custom agents (`.agent.md`), prompts (`.prompt.md`), or instruction files (`.instructions.md`)
- Configure MCP servers for external tool access
- Choose the right customization method for your needs
- Set up the `.github/` folder structure

## Quick Decision Guide

```
Need to...
├─ Apply rule to ALL code? → copilot-instructions.md
├─ Apply rule to specific file types? → .instructions.md  
├─ Create reusable workflow? → .agent.md
├─ Template a common task? → .prompt.md
├─ Package domain knowledge? → SKILL.md
└─ Add external tools? → mcp.json (+ MCP server)
```

## Six Customization Methods

| Method | Extension | When to Use | Details |
|--------|-----------|-------------|---------|
| **Workspace Instructions** | `.github/copilot-instructions.md` | Project-wide baseline rules | [Guide](references/detailed-guide.md#workspace-instructions) |
| **Agents** | `.agent.md` | Task-specific workflows with tools | [Guide](references/detailed-guide.md#custom-agents) · [Examples](references/agent-examples.md) |
| **Prompts** | `.prompt.md` | Reusable task templates | [Guide](references/detailed-guide.md#prompt-files) |
| **Instructions** | `.instructions.md` | File-type conditional rules | [Guide](references/detailed-guide.md#instruction-files) · [Examples](references/instruction-examples.md) |
| **Skills** | `SKILL.md` | Domain knowledge packages | [Guide](references/detailed-guide.md#agent-skills) |
| **MCP Servers** | `.vscode/mcp.json` | External tool integration | [Setup Guide](references/mcp-setup.md) |

**Critical**: Use exact file extensions or detection fails.

## Prerequisites

- VS Code with GitHub Copilot extension
- Enable instruction files in settings:
  ```json
  {
    "github.copilot.chat.codeGeneration.useInstructionFiles": true,
    "chat.agent.enabled": true
  }
  ```

## Directory Structure

```
.github/
├── copilot-instructions.md
├── agents/
│   ├── planner.agent.md
│   └── reviewer.agent.md
├── prompts/
│   └── generate-component.prompt.md
├── instructions/
│   ├── python-coding.instructions.md
│   └── typescript-coding.instructions.md
└── skills/
    └── <skill-name>/SKILL.md

.vscode/
└── mcp.json  # VS Code only
```

## Quick Start

1. **Create workspace baseline**: [Copy template](templates/copilot-instructions.template.md) to `.github/copilot-instructions.md`
2. **Add custom agent**: [Use template](templates/agent.template.md) → save as `.github/agents/<name>.agent.md`
3. **Create prompt**: [Use template](templates/prompt.template.md) → save as `.github/prompts/<name>.prompt.md`
4. **Add instruction file**: [Use template](templates/instructions.template.md) → save as `.github/instructions/<name>.instructions.md`
5. **Configure MCP**: See [MCP Setup Guide](references/mcp-setup.md)

## Details and Examples

### Complete Guides
- [Detailed Guides](references/detailed-guide.md) - In-depth information on all methods
  - Agent frontmatter properties (9 properties with handoffs)
  - Available models and tools
  - Prompt file properties
  - Glob patterns for instruction files
  - Skills vs Instructions comparison
  - Combining methods patterns
- [Agent Examples](references/agent-examples.md) - Common patterns (Planner, Implementer, Reviewer)
- [Instruction Examples](references/instruction-examples.md) - Language/framework specific
- [Chat Tools Reference](references/chat-tools.md) - Complete list of 47+ tools and tool sets
- [VS Code Settings](references/recommended-settings.md) - Essential Copilot settings organized by category
- [MCP Setup](references/mcp-setup.md) - Complete MCP server configuration guide with stdio/HTTP types

### Templates
- [Agent Template](templates/agent.template.md) - Generic `.agent.md` starter
- [Prompt Template](templates/prompt.md) - Generic `.prompt.md` starter  
- [Instructions Template](templates/instructions.template.md) - Generic `.instructions.md` starter
- [Copilot Instructions Template](templates/copilot-instructions.template.md) - Workspace baseline starter

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Instructions not applied | Enable `useInstructionFiles` in settings |
| Agent not visible | Check `.agent.md` extension, verify YAML syntax |
| Prompt not appearing | Ensure `.prompt.md` extension |
| Instruction file ignored | Verify `.instructions.md` extension, test glob pattern |
| MCP server not starting | Check command/args, view MCP output logs |
| Tool not available | Verify tool in agent's `tools` list or MCP server running |

## External Resources

- [Custom Agents Documentation](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- [Agent Skills Documentation](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Custom Instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
- [Prompt Files](https://code.visualstudio.com/docs/copilot/customization/prompt-files)
- [Chat Tools Reference](https://code.visualstudio.com/docs/copilot/reference/copilot-vscode-features#chat-tools)
- [MCP Servers](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
- [Agent Skills Standard](https://agentskills.io/)
