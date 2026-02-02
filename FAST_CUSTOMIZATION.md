# Fast Customization Guide

This guide covers the new features in Custom Copilot (cuco) that enable fast and quick customization of Agentic Coding Agents for your project.

## Overview

Custom Copilot now supports multiple integration engines and standards, making it easy to work with various agentic coding platforms and share resources across projects and teams.

## Integration Engines

### Supported Engines

1. **GitHub Copilot** (`.github/` folder) - Default
   - Full GitHub Copilot customization support
   - Agents, prompts, skills, instructions
   - `copilot-instructions.md` for workspace baseline

2. **Claude Code** (`.claude/` folder)
   - Claude Code customization format
   - Agents, prompts, skills
   - `instructions.md` for workspace configuration

3. **Tool-Agnostic** (`.cuco/` folder)
   - Universal format that works with any tool
   - Includes bundles and MCP configurations
   - Can be synced to other formats

### Initializing a Project

```bash
# Initialize for GitHub Copilot (default)
cuco init

# Initialize for Claude Code
cuco init --engine=claude

# Initialize for tool-agnostic format
cuco init --engine=cuco
```

## Creating Resources from Templates

### Template Command

The `cuco template` command helps you quickly create new resources without starting from scratch.

```bash
# List available templates
cuco template list

# Create an agent
cuco template create agent my-coding-agent

# Create a skill
cuco template create skill my-workflow-skill

# Create a prompt
cuco template create prompt my-task-prompt

# Create a bundle
cuco template create bundle my-project-bundle
```

### Customizing Templates

After creating from a template:

1. Navigate to the created file/folder
2. Edit the content to match your requirements
3. Update the YAML frontmatter (for agents, skills)
4. Add specific instructions and examples
5. Test with your agentic coding tool

### Template Locations

Resources are created in your active integration folder:
- `.github/agents/`, `.github/skills/`, etc.
- `.claude/agents/`, `.claude/skills/`, etc.
- `.cuco/agents/`, `.cuco/skills/`, etc.

## Publishing Resources

### Publishing to CUCO Marketplace

Share your resources with the community:

```bash
cuco publish ./my-skill --type=skill --source=marketplace
```

This provides step-by-step instructions for:
1. Forking the repository
2. Copying your resource
3. Creating a Pull Request

### Publishing to Git Repositories

Publish directly to a git repository with a commit:

```bash
cuco publish ./my-agent.agent.md \
  --type=agent \
  --source=git-commit \
  --destination=/path/to/repo/agents \
  --message="Add new coding agent"
```

### Publishing to Local Directories

Copy resources to a local directory:

```bash
cuco publish ./my-skill \
  --type=skill \
  --source=local \
  --destination=/path/to/destination
```

## Working with Multiple Standards

### Supported Standards

1. **AgentSkills.io** - Skills with `SKILL.md` format
   - Already fully supported
   - Works with anthropics/skills and compatible repos
   - See [AGENTSKILLS.md](AGENTSKILLS.md)

2. **GitHub Copilot** - `.github/` folder structure
   - Native support for GitHub Copilot
   - Agents, prompts, skills, instructions
   - MCP server integration

3. **Claude Code** - `.claude/` folder structure
   - NEW: Native support for Claude Code
   - Simplified structure without instructions subfolder

4. **MCP (Model Context Protocol)** - Server configurations
   - Already fully supported
   - Managed in `.vscode/mcp.json`
   - See mcp-builder skill

### Consuming Resources from Different Sources

#### From CUCO Marketplace

```bash
# Add from built-in registry
cuco add skill test-driven-development
cuco add agent skill-builder
```

#### From GitHub URLs (AgentSkills.io compatible)

```bash
# From anthropics/skills
cuco add skill https://github.com/anthropics/skills/tree/main/skills/brand-guidelines

# From any public repo
cuco add skill https://github.com/owner/repo/tree/main/skills/my-skill
```

#### From Private Repositories

```bash
# Add your private source
cuco source add my-company https://github.com/mycompany/copilot-customs.git

# Use resources from it
cuco add skill company-workflow
cuco add agent company-coding-assistant
```

#### From Bundles

Bundles can include resources from multiple sources:

```json
{
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
      }
    ]
  }
}
```

## Advanced Features

### Bundle Resources for Effectiveness

Create bundles that combine resources that work well together:

```bash
# Create a bundle template
cuco template create bundle my-complete-setup

# Edit the bundle.json to include:
# - Related skills
# - Supporting agents
# - Custom prompts
# - Workspace instructions (copilot-instructions.md)
```

### Sync with Conflict Detection

Keep resources up-to-date while preserving customizations:

```bash
# Sync all resources
cuco sync

# Sync specific resource
cuco sync skill-name
```

When local modifications are detected:
- You'll be prompted to choose
- Option 1: Overwrite with registry version
- Option 2: Keep local version

### Custom Repository Structures

Your private repositories can use any of these structures:

```
# Traditional CUCO
repo/
└── custom_copilot/
    ├── agents/
    ├── skills/
    └── bundles/

# Tool-agnostic
repo/
└── .cuco/
    ├── agents/
    ├── skills/
    └── bundles/

# GitHub Copilot
repo/
└── .github/
    ├── agents/
    └── skills/

# Claude Code
repo/
└── .claude/
    ├── agents/
    └── skills/

# AgentSkills.io
repo/
└── skills/
    ├── skill-one/
    │   └── SKILL.md
    └── skill-two/
        └── SKILL.md
```

## Best Practices

### Creating Effective Resources

1. **Use Templates** - Start with templates for consistency
2. **Clear Descriptions** - Write clear YAML frontmatter
3. **Specific Instructions** - Be precise in your instructions
4. **Include Examples** - Add usage examples
5. **Test Thoroughly** - Validate with your agentic tool

### Organizing Projects

1. **Start with Init** - Initialize the appropriate engine
2. **Use Bundles** - Group related resources
3. **Leverage Sources** - Set up private sources for team resources
4. **Version Control** - Track customizations in git
5. **Document Usage** - Add README files to custom bundles

### Sharing Resources

1. **Validate First** - Ensure resources work before publishing
2. **Clear Naming** - Use descriptive names
3. **Include Metadata** - Complete all metadata fields
4. **Provide Examples** - Show how to use the resource
5. **Follow Standards** - Adhere to AgentSkills.io or other standards

## Migration Guide

### From .github/ to .claude/

```bash
# Initialize Claude structure
cuco init --engine=claude

# Copy agents
cp -r .github/agents/* .claude/agents/

# Copy skills
cp -r .github/skills/* .claude/skills/

# Copy prompts
cp -r .github/prompts/* .claude/prompts/

# Merge instructions
cat .github/copilot-instructions.md >> .claude/instructions.md
```

### From .github/ to .cuco/

```bash
# Initialize tool-agnostic structure
cuco init --engine=cuco

# Use cuco to copy resources
# Resources will automatically go to detected target directory
```

## Examples

### Complete Workflow: Creating and Publishing a Skill

```bash
# 1. Initialize project
cuco init

# 2. Create skill from template
cuco template create skill my-api-documentation

# 3. Edit the skill
vim .github/skills/my-api-documentation/SKILL.md

# 4. Test the skill
# (Use GitHub Copilot to test)

# 5. Publish to marketplace
cuco publish .github/skills/my-api-documentation \
  --type=skill \
  --source=marketplace
```

### Setting Up Team Resources

```bash
# 1. Initialize project
cuco init

# 2. Add company source
cuco source add our-team git@github.com:company/ai-resources.git

# 3. Install team bundle
cuco bundle add team-standards

# 4. Add individual team resources
cuco add skill code-review-process
cuco add agent architecture-advisor

# 5. Customize for project
cuco template create skill project-specific-workflow
```

### Multi-Engine Setup

```bash
# 1. Initialize all engines
cuco init --engine=github
cuco init --engine=claude
cuco init --engine=cuco

# 2. Use .cuco/ as central source
cuco template create skill universal-skill
# Edit in .cuco/skills/universal-skill/

# 3. Copy to specific engines as needed
cp -r .cuco/skills/universal-skill .github/skills/
cp -r .cuco/skills/universal-skill .claude/skills/
```

## Troubleshooting

### Templates Not Found

**Problem**: `Error: Template 'X' not found`

**Solution**: Ensure custom-copilot is properly installed:
```bash
pip install -e /path/to/custom-copilot
```

### Wrong Target Directory

**Problem**: Resources created in wrong folder

**Solution**: Check which folders exist. CUCO auto-detects in this order:
1. `.github/`
2. `.claude/`
3. `.cuco/`

### Publish Validation Errors

**Problem**: Resource fails validation

**Solution**: 
- Agents must end with `.agent.md`
- Prompts must end with `.prompt.md`
- Skills must have `SKILL.md` file
- Bundles must have `bundle.json` file

## Next Steps

- Explore [AgentSkills Integration](AGENTSKILLS.md)
- Read [Quick Reference](QUICK_REFERENCE.md)
- Check out example bundles in `custom_copilot/bundles/`
- Join the community and share your resources!

## Resources

- [Custom Copilot Repository](https://github.com/DJ2695/custom-copilot)
- [AgentSkills.io](https://agentskills.io)
- [Anthropic Skills](https://github.com/anthropics/skills)
- [MCP Documentation](https://modelcontextprotocol.io)
