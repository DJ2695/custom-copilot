# Migration Guide: Legacy Registry to Copilot Customizations

This guide helps you understand the new copilot-customizations structure and how to migrate if needed.

## What Changed?

### New Directory Structure

**Before:**
```
src/cc/registry/
├── agents/
├── prompts/
├── instructions/
└── skills/
```

**After:**
```
copilot-customizations/
├── agents/
│   ├── latest/          # Current stable version
│   └── v1/              # Version 1 for compatibility
├── prompts/
│   ├── latest/
│   └── v1/
├── skills/
│   └── latest/
├── instructions/
│   └── latest/
└── bundles/             # NEW: Pre-configured combinations
    ├── example-bundle/
    └── development-essentials/
```

### Why This Change?

1. **Versioning Support**: Keep multiple versions of resources for compatibility
2. **Bundle System**: Pre-configured combinations that work together
3. **Separation of Concerns**: 
   - `.github/` for development and testing
   - `copilot-customizations/` for stable, versioned distribution
4. **Better Organization**: Clear structure for managing resources at scale

## Impact on Users

### For End Users (Installing Artifacts)

**No action required!** The existing commands continue to work:

```bash
cuco add agent skill-builder    # Still works
cuco add skill test-driven-development  # Still works
cuco sync                        # Still works
```

The legacy `src/cc/registry/` is maintained for backward compatibility.

### New Features Available

You can now use bundles:

```bash
# List available bundles
cuco bundle list
cuco list bundles

# Install a bundle (includes all dependencies)
cuco bundle add development-essentials
```

## For Contributors

### Old Workflow (Still Supported)

```bash
# Add new resource to registry
cp my-skill/ src/cc/registry/skills/
```

### New Workflow (Recommended)

#### 1. Development Phase (Use `.github/`)

Develop and test in `.github/` folder:

```bash
# Create new skill in .github for testing
mkdir .github/skills/my-new-skill
# ... develop and test ...
```

#### 2. Promotion Phase (Move to `copilot-customizations/`)

Once stable, promote to versioned structure:

```bash
# Copy to latest version
cp -r .github/skills/my-new-skill copilot-customizations/skills/latest/

# Create v1 for compatibility (optional)
cp -r copilot-customizations/skills/latest/my-new-skill copilot-customizations/skills/v1/
```

#### 3. Bundle Creation (Optional)

Create a bundle that includes your resource:

```bash
# Create bundle directory
mkdir -p copilot-customizations/bundles/my-bundle

# Create manifest
cat > copilot-customizations/bundles/my-bundle/bundle.json << 'EOF'
{
  "name": "my-bundle",
  "version": "1.0.0",
  "description": "My custom bundle",
  "dependencies": {
    "skills": [
      {
        "name": "my-new-skill",
        "type": "reference",
        "source": "skills/latest/my-new-skill",
        "version": "latest"
      }
    ]
  }
}
EOF
```

## Version Management

### When to Create a New Version

Create a new version (v2, v3, etc.) when:
- Making breaking changes to a resource
- Supporting different copilot versions
- Maintaining backward compatibility

### Example: Creating v2 of a Skill

```bash
# Copy current latest to v1 (preserve old version)
cp -r copilot-customizations/skills/latest/my-skill copilot-customizations/skills/v1/

# Update latest with new version
# Make your breaking changes to copilot-customizations/skills/latest/my-skill
```

### Referencing Specific Versions in Bundles

```json
{
  "dependencies": {
    "skills": [
      {
        "name": "my-skill",
        "type": "reference",
        "source": "skills/v1/my-skill",  // Pin to v1
        "version": "v1"
      }
    ]
  }
}
```

## Bundle Types

### 1. Pure Reference Bundle

Only references existing resources:

```json
{
  "name": "reference-bundle",
  "dependencies": {
    "agents": [
      {
        "name": "skill-builder",
        "type": "reference",
        "source": "agents/latest/skill-builder.agent.md",
        "version": "latest"
      }
    ]
  }
}
```

### 2. Mixed Bundle

Combines references and inline resources:

```json
{
  "name": "mixed-bundle",
  "dependencies": {
    "agents": [
      {
        "name": "skill-builder",
        "type": "reference",          // From central registry
        "source": "agents/latest/skill-builder.agent.md"
      }
    ],
    "prompts": [
      {
        "name": "custom-prompt",
        "type": "inline",              // Bundle-specific
        "path": "prompts/custom.prompt.md"
      }
    ]
  }
}
```

### 3. Standalone Bundle

All resources inline (bundle-specific):

```json
{
  "name": "standalone-bundle",
  "dependencies": {
    "skills": [
      {
        "name": "bundle-specific-skill",
        "type": "inline",
        "path": "skills/bundle-specific-skill"
      }
    ]
  }
}
```

## Best Practices

### For Resource Creators

1. **Develop in `.github/`** - Test thoroughly before promoting
2. **Promote to `latest/`** - Once stable
3. **Create versions only when needed** - Don't version prematurely
4. **Document breaking changes** - When creating new versions
5. **Use semantic versioning in bundles** - Follow semver principles

### For Bundle Creators

1. **Reference stable versions** - Use `latest/` or specific versions
2. **Document dependencies** - Explain why resources are combined
3. **Test bundle installation** - Verify all dependencies install correctly
4. **Include copilot-instructions.md** - Explain how to use the bundle
5. **Version your bundles** - Update bundle version when changing dependencies

## Troubleshooting

### Bundle Installation Fails

**Error:** "Referenced resource not found"

**Solution:** Ensure the source path in bundle.json matches the actual file location:

```json
{
  "source": "agents/latest/skill-builder.agent.md"  // Correct
  // NOT: "../../agents/latest/skill-builder.agent.md"
}
```

### Version Conflicts

**Problem:** Different bundles need different versions of the same resource

**Solution:** 
1. Create separate version folders (v1, v2)
2. Reference specific versions in each bundle
3. Or, use inline resources for bundle-specific variations

## FAQ

**Q: Will the old `src/cc/registry/` be removed?**  
A: Not immediately. It's maintained for backward compatibility but new resources should go in `copilot-customizations/`.

**Q: Can I mix old and new approaches?**  
A: Yes! You can use `cuco add` for individual resources and `cuco bundle add` for bundles.

**Q: How do I update an existing resource?**  
A: Update the file in `copilot-customizations/<type>/latest/` and consider creating a new version folder for the old version.

**Q: Can bundles reference other bundles?**  
A: Not currently, but this is a planned feature.

**Q: What happens if I modify a bundle-installed resource?**  
A: Currently, `cuco sync` doesn't track bundle resources. This is being improved.

## Getting Help

- Check the main [README.md](README.md) for detailed documentation
- Review [copilot-customizations/README.md](copilot-customizations/README.md) for structure details
- Look at example bundles in `copilot-customizations/bundles/`

## Summary

The new structure provides:
- ✅ Version management
- ✅ Bundle system for combining resources
- ✅ Clear separation between development and distribution
- ✅ Backward compatibility with existing commands
- ✅ Better organization at scale

Start using bundles today with `cuco bundle list`!
