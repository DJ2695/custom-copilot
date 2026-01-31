---
agent: 'agent'
model: Claude Opus 4.5
tools: ['codebase', 'edit', 'createFile']
description: '[One-line task description]'
---

# [Task Name]

[Brief explanation of what this accomplishes]

## Questions

Ask user if missing:
- [Required input 1]
- [Required input 2]

## Requirements

- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

## Output

[Expected structure, format, and quality criteria]

---

<!-- 
CUSTOMIZATION GUIDE:
- agent='agent' for code gen, agent='ask' for analysis
- Select tools from: references/chat-tools.md
- Reference: #tool:githubRepo org/repo
- Reference: [file.md](../docs/file.md)
-->
