# Quick Reference: Copilot Customizations & Bundles

## Quick Start

```bash
# Initialize project
cuco init

# List available bundles
cuco bundle list

# Install a bundle (recommended for quick start)
cuco bundle add development-essentials
```

## Commands Overview

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

```
your-project/
└── .github/
    ├── agents/
    ├── prompts/
    ├── instructions/
    ├── skills/
    └── copilot-instructions.md
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

## Resource Versioning

Resources are versioned in `copilot-customizations/`:

```
copilot-customizations/
├── agents/
│   ├── latest/    # Current stable version
│   └── v1/        # Version 1
├── prompts/
│   ├── latest/
│   └── v1/
└── skills/
    └── latest/
```

**Bundles can reference specific versions:**
- `latest/` - Current stable (recommended)
- `v1/`, `v2/` - Specific versions for compatibility

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
3. **Promote** to `copilot-customizations/latest/` when stable
4. **Create version** (`v1/`, `v2/`) if needed for compatibility
5. **Bundle** related resources for distribution

## Common Workflows

### Starting a New Project

```bash
cd my-project
cuco init
cuco bundle add development-essentials
# Start coding with TDD, debugging, and skill creation support
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
# 1. Create bundle directory
mkdir -p copilot-customizations/bundles/my-bundle

# 2. Create manifest
cat > copilot-customizations/bundles/my-bundle/bundle.json << 'EOF'
{
  "name": "my-bundle",
  "version": "1.0.0",
  "description": "My custom bundle",
  "dependencies": {
    "skills": [
      {
        "name": "my-skill",
        "type": "reference",
        "source": "skills/latest/my-skill",
        "version": "latest"
      }
    ]
  }
}
EOF

# 3. Add instructions
cat > copilot-customizations/bundles/my-bundle/copilot-instructions.md << 'EOF'
# My Bundle
Instructions on how to use this bundle...
EOF
```

## Getting Help

- **Full documentation:** [README.md](README.md)
- **Migration guide:** [MIGRATION.md](MIGRATION.md)
- **Structure details:** [copilot-customizations/README.md](copilot-customizations/README.md)
- **Command help:** `cuco help`

## Tips

💡 **Bundle vs Individual Resources**
- Use bundles for quick setup with related resources
- Use individual resources for precise control

💡 **Versioning**
- Stick with `latest/` unless you need specific compatibility
- Create versions when making breaking changes

💡 **Development**
- Use `.github/` for experimentation
- Promote to `copilot-customizations/` when stable

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
