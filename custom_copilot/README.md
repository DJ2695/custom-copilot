# Custom Copilot Resources

This directory contains copilot customizations including agents, prompts, skills, instructions, bundles, and templates.

## Directory Structure

```
custom_copilot/
├── agents/           # Custom agents (no versioning)
├── prompts/          # Reusable prompts (no versioning)
├── skills/           # Skills (no versioning)
├── instructions/     # Instructions (no versioning)
├── bundles/          # Pre-configured bundles (with versioning)
└── templates/        # Templates for creating new resources
```

## Resources (No Versioning)

Base resources (agents, prompts, skills, instructions) are stored without version folders. This keeps the structure simple and clean. When a resource needs updates, it's updated in place.

### Agents

Custom agents with specialized capabilities. Each agent is a `.agent.md` file.

**Example:**
```
agents/
└── skill-builder.agent.md
```

### Prompts

Reusable prompts for common tasks. Each prompt is a `.prompt.md` file.

**Example:**
```
prompts/
├── git.prompt.md
└── remember.prompt.md
```

### Skills

Skills provide specialized knowledge and workflows. Each skill is a directory containing a `SKILL.md` file.

**Example:**
```
skills/
├── test-driven-development/
│   └── SKILL.md
└── skill-creator/
    └── SKILL.md
```

### Instructions

General instructions for copilot. Each instruction is a `.md` file.

**Example:**
```
instructions/
└── sample.md
```

## Bundles (With Versioning)

Bundles are pre-configured combinations of resources. Each bundle can have multiple versions.

**Structure:**
```
bundles/
└── development-essentials/
    ├── v1.0.0/              # Versioned
    │   ├── bundle.json
    │   └── copilot-instructions.md
    └── v1.1.0/              # New version
        ├── bundle.json
        └── copilot-instructions.md
```

**Current bundles (flat, can be versioned later):**
```
bundles/
├── development-essentials/
│   ├── bundle.json
│   └── copilot-instructions.md
└── example-bundle/
    ├── bundle.json
    └── copilot-instructions.md
```

### Bundle Manifest

Each bundle has a `bundle.json` manifest that defines dependencies:

```json
{
  "name": "bundle-name",
  "version": "1.0.0",
  "dependencies": {
    "agents": [
      {
        "name": "agent-name",
        "type": "reference",
        "source": "agents/agent-name.agent.md"
      }
    ],
    "prompts": [...],
    "skills": [...],
    "instructions": [...]
  }
}
```

**Resource Types:**
- **reference**: Links to a resource in the main directories (agents/, prompts/, etc.)
- **inline**: Bundle-specific resource included in the bundle directory

## Templates

The `templates/` directory contains templates for creating new resources:

```
templates/
├── agent-template.agent.md
├── prompt-template.prompt.md
├── skill-template/
│   └── SKILL.md
└── bundle-template/
    ├── bundle.json
    └── copilot-instructions.md
```

### Using Templates

1. Copy the appropriate template
2. Rename and customize for your use case
3. Place in the appropriate directory (agents/, prompts/, skills/, etc.)

## Usage with `cuco` CLI

```bash
# List resources
cuco list agents
cuco list prompts
cuco list skills
cuco list bundles

# Add individual resource
cuco add agent skill-builder
cuco add prompt git
cuco add skill test-driven-development

# Install bundle
cuco bundle add development-essentials
```

## Design Principles

1. **Flat structure for base resources** - No version folders, resources updated in place
2. **Versioning only for bundles** - Bundles can be versioned when needed
3. **Template-driven** - Templates make creating new resources easy
4. **Reference-based bundles** - Bundles reference shared resources, avoiding duplication

## Creating New Resources

### New Agent

1. Copy `templates/agent-template.agent.md`
2. Rename to `agents/your-agent.agent.md`
3. Customize the content
4. Commit to repository

### New Skill

1. Copy `templates/skill-template/` directory
2. Rename to `skills/your-skill/`
3. Customize `SKILL.md`
4. Add any reference files
5. Commit to repository

### New Bundle

1. Copy `templates/bundle-template/` directory
2. Rename to `bundles/your-bundle/`
3. Customize `bundle.json` with dependencies
4. Customize `copilot-instructions.md`
5. Add any inline resources (optional)
6. Commit to repository

## Versioning Strategy

**Base Resources (agents, prompts, skills, instructions):**
- No versioning - updated in place
- Breaking changes should be rare
- If needed, create a new resource with a different name

**Bundles:**
- Can be versioned by creating version subdirectories
- Example: `bundles/my-bundle/v1.0.0/` and `bundles/my-bundle/v1.1.0/`
- Users can install specific bundle versions
- Allows gradual migration and compatibility

## Migration from Previous Structure

The previous `copilot-customizations/` structure with version folders has been simplified:

**Before:**
```
copilot-customizations/
├── agents/
│   ├── latest/
│   └── v1/
└── prompts/
    ├── latest/
    └── v1/
```

**After:**
```
custom_copilot/
├── agents/          # Flattened, no version folders
└── prompts/         # Flattened, no version folders
```

This simplification makes the structure cleaner and easier to maintain, while still supporting bundle versioning when needed.
