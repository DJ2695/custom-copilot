# Copilot Customizations

This directory contains versioned copilot customizations including agents, prompts, instructions, skills, and bundles.

## Directory Structure

```
copilot-customizations/
├── agents/           # Custom agents with version support
├── prompts/          # Reusable prompts with version support
├── instructions/     # Copilot instructions with version support
├── skills/           # Skills with version support
└── bundles/          # Pre-configured bundles combining multiple resources
```

## Versioning

Resources can be organized with version folders to support different copilot versions or iterations:

```
agents/
├── v1/
│   └── planner.agent.md
├── v2/
│   └── planner.agent.md
└── latest/
    └── planner.agent.md
```

## Bundles

Bundles are pre-configured combinations of copilot customizations that work together. Each bundle includes:
- A `bundle.json` manifest defining the bundle
- Referenced or inline resources (agents, prompts, instructions, skills)
- Dependency information ensuring all required resources are available

### Bundle Structure

```
bundles/
└── flutter-development/
    ├── bundle.json                    # Bundle manifest
    ├── copilot-instructions.md        # Bundle-specific instructions
    ├── agents/                        # Bundle-specific agents (optional)
    ├── prompts/                       # Bundle-specific prompts (optional)
    └── skills/                        # Bundle-specific skills (optional)
```

### Bundle Manifest (bundle.json)

```json
{
  "name": "flutter-development",
  "version": "1.0.0",
  "description": "Complete Flutter development bundle with clean architecture",
  "copilotInstructions": {
    "type": "inline",
    "path": "copilot-instructions.md"
  },
  "dependencies": {
    "agents": [
      {
        "name": "skill-builder",
        "type": "reference",
        "source": "agents/v1/skill-builder.agent.md",
        "version": "v1"
      }
    ],
    "prompts": [
      {
        "name": "git",
        "type": "reference",
        "source": "prompts/v1/git.prompt.md",
        "version": "v1"
      }
    ],
    "skills": [
      {
        "name": "flutter-testing",
        "type": "inline",
        "path": "skills/flutter-testing"
      },
      {
        "name": "test-driven-development",
        "type": "reference",
        "source": "skills/v1/test-driven-development",
        "version": "v1"
      }
    ]
  }
}
```

### Resource Types

- **reference**: Links to a versioned resource in the main customizations folders
- **inline**: Contains bundle-specific customizations included directly in the bundle

## Usage with `cuco` CLI

```bash
# Add a bundle to your project
cuco add bundle flutter-development

# List available bundles
cuco list bundles

# Sync bundle dependencies
cuco sync bundle flutter-development
```

## Developing New Resources

The `.github` folder remains available for developing and testing new skills, agents, instructions, and prompts before adding them to the versioned customizations.

```
.github/
├── agents/           # Development/testing agents
├── prompts/          # Development/testing prompts
├── skills/           # Development/testing skills
└── copilot-instructions.md
```

Once resources are stable, they can be promoted to `copilot-customizations/` with proper versioning.
