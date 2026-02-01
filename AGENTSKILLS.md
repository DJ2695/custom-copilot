# AgentSkills.io Integration

Custom Copilot (cuco) fully supports the [agentskills.io](https://agentskills.io) standard, enabling seamless integration with skills from repositories like [anthropics/skills](https://github.com/anthropics/skills) and any other agentskills-compatible repository.

## What is AgentSkills.io?

AgentSkills.io is a standard for creating skills that teach AI agents how to complete specific tasks in a repeatable way. Skills are folders containing:

- A `SKILL.md` file with YAML frontmatter and instructions
- Optional reference materials, scripts, and other resources

The standard format looks like:

```markdown
---
name: skill-name
description: What the skill does and when to use it
---

# Skill Instructions

[Instructions that the AI agent will follow]
```

## Using AgentSkills with cuco

### Adding Skills from GitHub URLs

You can add any skill from an agentskills-compatible repository using its GitHub URL:

```bash
# Add a skill from anthropics/skills
cuco add skill https://github.com/anthropics/skills/tree/main/skills/brand-guidelines

# Add from any agentskills repo
cuco add skill https://github.com/owner/repo/tree/main/skills/my-skill
```

### Using the AgentSkills Bundle Type

In bundles, use the `agentskills` source type to reference skills from agentskills repositories:

```json
{
  "dependencies": {
    "skills": [
      {
        "name": "doc-coauthoring",
        "type": "agentskills",
        "repo": "anthropics/skills",
        "skill": "doc-coauthoring"
      }
    ]
  }
}
```

### Example Bundle

Try the included `agentskills-example` bundle which demonstrates the integration:

```bash
cuco bundle add agentskills-example
```

This installs skills from the anthropics/skills repository:
- **doc-coauthoring**: Structured workflow for co-authoring documentation
- **mcp-builder**: Guide for creating MCP servers
- **skill-creator**: Guide for creating effective skills

## Repository Structure Support

Custom Copilot supports multiple repository structures, making it compatible with various skill distribution methods:

### AgentSkills.io Standard
```
repo/
└── skills/
    ├── skill-one/
    │   └── SKILL.md
    ├── skill-two/
    │   └── SKILL.md
    └── ...
```

### GitHub Copilot Standard
```
repo/
└── .github/
    ├── agents/
    ├── prompts/
    ├── skills/
    └── copilot-instructions.md
```

### Custom Copilot Standard
```
repo/
└── custom_copilot/
    ├── agents/
    ├── prompts/
    ├── skills/
    └── bundles/
```

### Alternative .cuco Structure
```
repo/
└── .cuco/
    ├── agents/
    ├── prompts/
    ├── skills/
    └── bundles/
```

## Bundle Source Types

Custom Copilot supports multiple source types for maximum flexibility:

### 1. `custom-copilot` - Built-in Registry
Resources from the custom-copilot package registry.

```json
{
  "name": "my-skill",
  "type": "custom-copilot",
  "source": "skills/my-skill"
}
```

### 2. `bundle` - Bundle-included Resources
Resources included within the bundle itself.

```json
{
  "name": "my-skill",
  "type": "bundle",
  "path": "skills/my-skill"
}
```

### 3. `custom` - Private Git Repositories
Resources from configured private git sources.

```json
{
  "name": "company-skill",
  "type": "custom",
  "source_name": "my-company",
  "source": "skills/company-skill"
}
```

### 4. `github` - Direct GitHub URLs
Resources from any public GitHub repository.

```json
{
  "name": "external-skill",
  "type": "github",
  "url": "https://github.com/owner/repo/tree/main/skills/skill-name"
}
```

### 5. `agentskills` - AgentSkills Repositories
Skills from agentskills.io compatible repositories.

```json
{
  "name": "anthropic-skill",
  "type": "agentskills",
  "repo": "anthropics/skills",
  "skill": "skill-name"
}
```

## Creating AgentSkills-Compatible Repositories

To create your own agentskills-compatible repository:

1. Create a `skills/` folder at the repository root
2. Create subfolders for each skill
3. Add a `SKILL.md` file with YAML frontmatter:

```markdown
---
name: my-custom-skill
description: Clear description of what the skill does and when to use it
---

# My Custom Skill

[Instructions and guidelines for the AI agent]

## Examples
- Example usage 1
- Example usage 2

## Guidelines
- Guideline 1
- Guideline 2
```

4. Optionally add reference materials, scripts, or other resources

### Sharing Your Skills

Once you have an agentskills-compatible repository, others can use it:

```bash
# Direct URL
cuco add skill https://github.com/yourorg/skills/tree/main/skills/my-skill

# Or add as a custom source
cuco source add yourorg https://github.com/yourorg/skills.git
cuco add skill my-skill

# Or reference in a bundle
{
  "dependencies": {
    "skills": [
      {
        "name": "my-skill",
        "type": "agentskills",
        "repo": "yourorg/skills",
        "skill": "my-skill"
      }
    ]
  }
}
```

## Benefits of the AgentSkills Standard

1. **Portability**: Skills work across different AI platforms
2. **Discoverability**: Standard structure makes skills easy to find and understand
3. **Reusability**: Share skills across projects and organizations
4. **Simplicity**: Minimal structure with maximum flexibility
5. **Ecosystem**: Build on skills from the community

## Resources

- [AgentSkills.io Website](https://agentskills.io)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [AgentSkills Specification](https://agentskills.io/specification)
- [Creating Custom Skills Guide](https://support.claude.com/en/articles/12512198-creating-custom-skills)

## Examples

### Adding Individual Skills

```bash
# From anthropics/skills
cuco add skill https://github.com/anthropics/skills/tree/main/skills/brand-guidelines
cuco add skill https://github.com/anthropics/skills/tree/main/skills/mcp-builder
cuco add skill https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring

# From your own repository
cuco add skill https://github.com/myorg/skills/tree/main/skills/my-skill
```

### Creating a Bundle with Multiple Sources

```json
{
  "name": "comprehensive-bundle",
  "version": "1.0.0",
  "description": "Bundle combining skills from multiple sources",
  "dependencies": {
    "skills": [
      {
        "name": "tdd",
        "type": "custom-copilot",
        "source": "skills/test-driven-development"
      },
      {
        "name": "brand-guidelines",
        "type": "agentskills",
        "repo": "anthropics/skills",
        "skill": "brand-guidelines"
      },
      {
        "name": "company-workflow",
        "type": "custom",
        "source_name": "my-company",
        "source": "skills/workflow"
      },
      {
        "name": "community-skill",
        "type": "github",
        "url": "https://github.com/community/skills/tree/main/skills/useful-skill"
      }
    ]
  }
}
```

## Frequently Asked Questions

### Q: Can I mix different source types in a bundle?
Yes! You can combine `custom-copilot`, `bundle`, `custom`, `github`, and `agentskills` sources in the same bundle.

### Q: Are skills cached?
Yes, repositories are cloned to `~/.cuco/repos/` and reused for subsequent operations, making repeated installations fast.

### Q: Can I use private repositories?
Yes, use the `custom` source type with authentication via git credentials or SSH keys.

### Q: What happens if a skill already exists?
You'll be prompted to confirm whether to overwrite the existing skill.

### Q: Can I contribute to the anthropics/skills repository?
Check the repository's contribution guidelines. Many skills are open source (Apache 2.0 license).
