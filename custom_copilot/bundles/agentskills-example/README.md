# AgentSkills Example Bundle

This bundle demonstrates integration with the [agentskills.io](https://agentskills.io) standard by including skills from the [anthropics/skills](https://github.com/anthropics/skills) repository.

## Included Skills

### doc-coauthoring
Guide users through a structured workflow for co-authoring documentation, proposals, technical specs, and decision docs.

### mcp-builder
Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services.

### skill-creator
Guide for creating effective skills that teach Claude how to complete specific tasks in a repeatable way.

## Installation

```bash
cuco bundle add agentskills-example
```

## Source Type

This bundle uses the `agentskills` source type, which is designed for repositories following the agentskills.io standard:

```json
{
  "name": "skill-name",
  "type": "agentskills",
  "repo": "owner/repo",
  "skill": "skill-folder-name"
}
```

## Features

- **Standards Compliance**: Works with any repository following the agentskills.io standard
- **Auto-cloning**: Automatically clones and caches the skills repository
- **SKILL.md Format**: All skills follow the standard SKILL.md format with YAML frontmatter
- **Reusability**: Once cached, skills from the same repo install instantly

## Creating Your Own AgentSkills Bundles

You can create bundles that reference any agentskills-compatible repository:

```json
{
  "dependencies": {
    "skills": [
      {
        "name": "my-skill",
        "type": "agentskills",
        "repo": "myorg/my-skills-repo",
        "skill": "my-skill-name"
      }
    ]
  }
}
```

The repository must follow this structure:

```
my-skills-repo/
└── skills/
    ├── my-skill-name/
    │   └── SKILL.md
    └── another-skill/
        └── SKILL.md
```
