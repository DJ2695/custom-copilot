# Quick Reference: Copilot Customizations & Bundles

## Quick Start

```bash
# Initialize project (GitHub Copilot)
cuco init

# Or initialize for Claude Code
cuco init --engine=claude

# Or initialize for tool-agnostic format
cuco init --engine=cuco

# List available bundles
cuco bundle list

# Install a bundle (recommended for quick start)
cuco bundle add development-essentials
```

## Commands Overview

### Initialization

```bash
cuco init                    # .github/ (GitHub Copilot - default)
cuco init --engine=claude    # .claude/ (Claude Code)
cuco init --engine=cuco      # .cuco/ (Tool-agnostic)
```

### Templates (NEW!)

```bash
# List templates
cuco template list

# Create from template
cuco template create agent my-agent
cuco template create skill my-skill
cuco template create prompt my-prompt
cuco template create bundle my-bundle
```

### Publishing (NEW!)

```bash
# Publish to marketplace
cuco publish ./my-skill --type=skill --source=marketplace

# Publish to git repository
cuco publish ./my-agent.agent.md --source=git-commit \
  --destination=/path/to/repo/agents --message="Add agent"

# Publish to local directory
cuco publish ./my-skill --source=local --destination=/path/to/dest
```

### Individual Resources

```bash
# List resources
cuco list agents
cuco list prompts
cuco list skills
cuco list instructions
cuco list mcps

# Add individual resource
cuco add agent skill-builder
cuco add prompt git
cuco add skill test-driven-development
cuco add mcp context7

# Sync resources
cuco sync                    # All tracked resources
cuco sync skill-builder      # Specific resource
```

### Bundles

```bash
# List bundles
cuco bundle list
cuco list bundles            # Alternative

# Install bundle
cuco bundle add <bundle-name>
```

## Available Bundles

### development-essentials
**Version:** 1.0.0  
**Description:** Essential development bundle with TDD, debugging, and skill creation tools

**Includes:**
- 1 Agent: skill-builder
- 1 Prompt: git
- 4 Skills: test-driven-development, systematic-debugging, skill-creator, subagent-driven-development

**Use when:** Starting a new project, need core development workflows

```bash
cuco bundle add development-essentials
```

### example-bundle
**Version:** 1.0.0  
**Description:** Example bundle demonstrating bundle structure

**Includes:**
- 1 Agent: skill-builder (reference)
- 2 Prompts: git (reference), custom-prompt (inline)
- 1 Skill: test-driven-development (reference)

**Use when:** Learning how bundles work, creating your own bundle

```bash
cuco bundle add example-bundle
```

## Directory Structure

### Project Structure After Init

**GitHub Copilot (.github/)**
```
your-project/
└── .github/
    ├── agents/
    ├── prompts/
    ├── instructions/
    ├── skills/
    └── copilot-instructions.md
```

**Claude Code (.claude/)**
```
your-project/
└── .claude/
    ├── agents/
    ├── prompts/
    ├── skills/
    └── instructions.md
```

**Tool-Agnostic (.cuco/)**
```
your-project/
└── .cuco/
    ├── agents/
    ├── prompts/
    ├── instructions/
    ├── skills/
    ├── bundles/
    ├── mcps/
    └── config.json
```

### After Installing development-essentials Bundle

```
your-project/
└── .github/
    ├── agents/
    │   └── skill-builder.agent.md
    ├── prompts/
    │   └── git.prompt.md
    ├── skills/
    │   ├── test-driven-development/
    │   ├── systematic-debugging/
    │   ├── skill-creator/
    │   └── subagent-driven-development/
    ├── instructions/
    └── copilot-instructions.md  (bundle-specific guidance)
```

## Resource Organization

Resources are organized in `custom_copilot/` with a flat structure:

```
custom_copilot/
├── agents/         # Flat, no version folders
├── prompts/        # Flat, no version folders
├── skills/         # Flat, no version folders
├── bundles/        # Can be versioned if needed
└── templates/      # Templates for new resources
```

**Base resources** are stored directly without version folders.  
**Bundles** can optionally be versioned when needed.

## Development Workflow

### For Users

1. Initialize: `cuco init`
2. Choose approach:
   - **Quick start:** `cuco bundle add development-essentials`
   - **Custom selection:** `cuco add skill <name>`, `cuco add agent <name>`
3. Start using GitHub Copilot with your customizations

### For Contributors

1. **Develop** in `.github/` folder
2. **Test** thoroughly
3. **Promote** to `custom_copilot/<type>/` when stable
4. **Use templates** from `custom_copilot/templates/`
5. **Bundle** related resources for distribution

## Common Workflows

### Starting a New Project

```bash
cd my-project
cuco init                         # Or init --engine=claude
cuco bundle add development-essentials
# Start coding with TDD, debugging, and skill creation support
```

### Creating Custom Resources

```bash
cuco template create skill my-custom-workflow
# Edit .github/skills/my-custom-workflow/SKILL.md
cuco template create agent my-coding-assistant
# Edit .github/agents/my-coding-assistant.agent.md
```

### Publishing Your Work

```bash
# Share with community
cuco publish ./my-skill --source=marketplace

# Publish to team repository
cuco publish ./my-agent.agent.md --source=git-commit \
  --destination=/path/to/team/repo/agents
```

### Adding Individual Resources

```bash
cuco list skills              # See what's available
cuco add skill skill-creator  # Add specific skill
```

### Keeping Resources Updated

```bash
cuco sync                     # Update all tracked resources
```

### Creating a Bundle (Contributors)

```bash
# 1. Use template
cp -r custom_copilot/templates/bundle-template custom_copilot/bundles/my-bundle

# 2. Edit manifest
cat > custom_copilot/bundles/my-bundle/bundle.json << 'EOF'
{
  "name": "my-bundle",
  "version": "1.0.0",
  "description": "My custom bundle",
  "dependencies": {
    "skills": [
      {
        "name": "my-skill",
        "type": "reference",
        "source": "skills/my-skill"
      }
    ]
  }
}
EOF

# 3. Edit instructions
cat > custom_copilot/bundles/my-bundle/copilot-instructions.md << 'EOF'
# My Bundle
Instructions on how to use this bundle...
EOF
```

## Getting Help

- **Fast Customization Guide:** [FAST_CUSTOMIZATION.md](FAST_CUSTOMIZATION.md) - NEW!
- **Full documentation:** [README.md](README.md)
- **AgentSkills Integration:** [AGENTSKILLS.md](AGENTSKILLS.md)
- **Migration guide:** [MIGRATION.md](MIGRATION.md)
- **Structure details:** [custom_copilot/README.md](custom_copilot/README.md)
- **Command help:** `cuco help`

## Tips

💡 **Integration Engines**
- GitHub Copilot: `.github/` folder (default)
- Claude Code: `.claude/` folder
- Tool-agnostic: `.cuco/` folder

💡 **Templates**
- Quick creation of agents, skills, prompts, bundles
- Use `cuco template create` for consistency
- Templates automatically use your active integration folder

💡 **Publishing**
- Share resources with marketplace or team
- Validation ensures quality before publishing
- Multiple destination options (marketplace, git, local)

💡 **Bundle vs Individual Resources**
- Use bundles for quick setup with related resources
- Use individual resources for precise control

💡 **Templates**
- Use templates in `custom_copilot/templates/` for consistency
- Templates include agent, prompt, skill, and bundle examples

💡 **Flat Structure**
- Base resources have no version folders
- Bundles can be versioned if needed
- Simpler and cleaner than nested versions

💡 **Development**
- Use `.github/` for experimentation
- Promote to `custom_copilot/` when stable

💡 **Syncing**
- Run `cuco sync` periodically to get updates
- Local modifications are detected and you'll be prompted

## Examples

### Example 1: Quick TDD Setup

```bash
cuco init
cuco bundle add development-essentials
# Now you have TDD skill, debugging skill, and skill-builder agent
```

### Example 2: Custom Selection

```bash
cuco init
cuco add skill test-driven-development
cuco add agent skill-builder
cuco add prompt git
# Manually selected resources
```

### Example 3: Update Existing Resources

```bash
cuco sync
# Updates all tracked resources if new versions available
# Prompts if you have local modifications
```

---

**Quick Links:**
- GitHub: https://github.com/DJ2695/custom-copilot
- Full README: [README.md](README.md)
- Migration Guide: [MIGRATION.md](MIGRATION.md)
