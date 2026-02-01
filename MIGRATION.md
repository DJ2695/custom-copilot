# Migration Guide: Professional Package with Private Repo Support

This guide explains the latest improvements to custom-copilot.

## Latest Changes (v0.2.0)

### Package Renamed

- **Old:** Package name was "copilot", module was "cc"
- **New:** Package name is "custom-copilot", module is "custom_copilot"

### Bundle Resource Types Updated

Resource types in bundle manifests have been renamed for clarity:

- **`custom-copilot`** (was "reference") - Resources from the custom-copilot repository
- **`bundle`** (was "inline") - Resources included within the bundle
- **`github`** (new) - Resources from 3rd party GitHub repos (future support)

**Example:**
```json
{
  "dependencies": {
    "agents": [
      {
        "name": "skill-builder",
        "type": "custom-copilot",
        "source": "agents/skill-builder.agent.md"
      }
    ],
    "prompts": [
      {
        "name": "custom",
        "type": "bundle",
        "path": "prompts/custom.prompt.md"
      }
    ]
  }
}
```

### Private Repository Support Added

You can now add custom sources for private customizations:

```bash
# Add your company's private repo
cuco source add company git https://github.com/mycompany/copilot-customs.git

# List sources
cuco source list

# Configuration is stored in ~/.cuco/config.json
```

## Previous Changes

### Directory Structure Simplified

**Previous (custom_copilot with versioning):**
```
custom_copilot/
├── agents/
│   ├── latest/          # Version folders added complexity
│   └── v1/
├── prompts/
│   ├── latest/
│   └── v1/
└── bundles/
```

**Current (custom_copilot flat structure):**
```
custom_copilot/
├── agents/              # Flat, no version folders
├── prompts/             # Flat, no version folders
├── skills/              # Flat, no version folders
├── instructions/        # Flat, no version folders
├── bundles/             # Can be versioned if needed
└── templates/           # NEW: Templates for creating resources
    ├── agent-template.agent.md
    ├── prompt-template.prompt.md
    ├── skill-template/
    └── bundle-template/
```

### Key Changes

1. **Flat structure** - No more `latest/` and `v1/` subfolders for base resources
2. **Templates added** - Easy to create new resources from templates
3. **Versioning only for bundles** - Bundles can be versioned when needed
4. **Cleaner paths** - `custom_copilot/agents/my-agent.agent.md` instead of `custom_copilot/agents/latest/my-agent.agent.md`

## Impact

### For End Users

✅ **No action required!** All commands work the same:

```bash
cuco init
cuco bundle list
cuco bundle add development-essentials
cuco add skill test-driven-development
cuco sync
```

### For Contributors

**Creating new resources is now easier:**

```bash
# Use templates
cp -r custom_copilot/templates/skill-template custom_copilot/skills/my-skill
# Edit my-skill/SKILL.md

# Or for agents
cp custom_copilot/templates/agent-template.agent.md custom_copilot/agents/my-agent.agent.md
```

**No more version folder management:**

```bash
# Old way (confusing)
cp my-skill/ custom_copilot/skills/latest/
cp my-skill/ custom_copilot/skills/v1/  # For compatibility

# New way (simple)
cp -r my-skill/ custom_copilot/skills/
```

## Bundle Manifest Changes

Bundle manifests now use simpler paths without version folders.

**Before:**
```json
{
  "dependencies": {
    "agents": [{
      "name": "skill-builder",
      "source": "agents/latest/skill-builder.agent.md",
      "version": "latest"
    }]
  }
}
```

**After:**
```json
{
  "dependencies": {
    "agents": [{
      "name": "skill-builder",
      "source": "agents/skill-builder.agent.md"
    }]
  }
}
```

Note: The `version` field is removed since resources are not versioned.

## Using Templates

The new `custom_copilot/templates/` directory makes creating resources easy:

### Creating a New Agent

```bash
# 1. Copy template
cp custom_copilot/templates/agent-template.agent.md custom_copilot/agents/my-agent.agent.md

# 2. Edit the file and customize
# 3. Test in .github/ folder first
# 4. When stable, it's ready to use
```

### Creating a New Skill

```bash
# 1. Copy template directory
cp -r custom_copilot/templates/skill-template custom_copilot/skills/my-skill

# 2. Edit my-skill/SKILL.md
# 3. Add any reference files
# 4. Test and deploy
```

### Creating a New Bundle

```bash
# 1. Copy template directory
cp -r custom_copilot/templates/bundle-template custom_copilot/bundles/my-bundle

# 2. Edit bundle.json with your dependencies
# 3. Edit copilot-instructions.md
# 4. Add any inline resources
```

## Versioning Strategy

### Base Resources (No Versioning)

Base resources are updated in place:

```
custom_copilot/agents/skill-builder.agent.md  # Updated in place
```

If you need different versions:
1. Use different names: `skill-builder-v2.agent.md`
2. Or version at the bundle level

### Bundles (Optional Versioning)

Bundles can be versioned when needed:

```
custom_copilot/bundles/
└── my-bundle/
    ├── v1.0.0/
    │   ├── bundle.json
    │   └── copilot-instructions.md
    └── v1.1.0/
        ├── bundle.json
        └── copilot-instructions.md
```

This is optional - most bundles don't need versioning.

## Migration Path

No migration required! The tool automatically uses the new structure.

### If You Were Developing Resources

Move from `.github/` to `custom_copilot/`:

```bash
# Develop in .github/
mkdir .github/skills/my-skill
# ... develop and test ...

# When stable, move to custom_copilot
cp -r .github/skills/my-skill custom_copilot/skills/
```

## Benefits

1. **Simpler** - No confusing version folders
2. **Cleaner** - Easier to navigate and understand
3. **Template-driven** - Consistent resource creation
4. **Flexible** - Bundles can still be versioned if needed
5. **Similar to Anthropic** - Follows industry patterns

## FAQ

**Q: What happened to versioning?**  
A: Base resources don't need versioning. They're updated in place. Bundles can be versioned if needed.

**Q: How do I support old and new versions?**  
A: Create separate resources with different names, or version at the bundle level.

**Q: Will my existing commands break?**  
A: No! All commands work the same. The CLI automatically uses the new structure.

**Q: Do I need to update my bundles?**  
A: Existing bundles in the repo have been updated. New bundles should use the flat path structure.

**Q: Where should I develop new resources?**  
A: Develop in `.github/` for testing, then promote to `custom_copilot/` when stable.

## Getting Help

- See [custom_copilot/README.md](custom_copilot/README.md) for structure details
- See [README.md](README.md) for CLI usage
- See templates in `custom_copilot/templates/` for examples
