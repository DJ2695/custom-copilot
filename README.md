# Custom Copilot (`cuco`)

A professional CLI tool for managing GitHub Copilot customizations including agents, prompts, skills, instructions, and bundles.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

## Features

- 🚀 **Easy Setup** - Initialize GitHub Copilot customizations in any project
- 📦 **Bundles** - Pre-configured combinations of customizations that work together
- 🔧 **Custom Sources** - Add private repositories for company-internal customizations
- 📝 **Templates** - Create new agents, prompts, skills, and bundles from templates
- 🔄 **Sync** - Keep your customizations up-to-date
- 🌐 **Extensible** - Support for public and private customization sources

## Quick Start

### Installation

```bash
# Install from GitHub
pip install git+https://github.com/DJ2695/custom-copilot.git

# Or clone and install locally
git clone https://github.com/DJ2695/custom-copilot.git
cd custom-copilot
pip install -e .
```

### Basic Usage

```bash
# Initialize a new project
cuco init

# Install a bundle
cuco bundle add development-essentials

# Add individual resources
cuco add skill test-driven-development
cuco add agent skill-builder

# List available resources
cuco list bundles
cuco list skills
```

## Documentation

- [Installation Guide](INSTALL.md) - Detailed installation instructions
- [Quick Reference](QUICK_REFERENCE.md) - Command reference and examples
- [Migration Guide](MIGRATION.md) - Upgrading from older versions

## Commands

### Project Setup

```bash
cuco init                    # Initialize .github folder structure
```

### Bundles

```bash
cuco bundle list             # List available bundles
cuco bundle add <name>       # Install a bundle
```

### Individual Resources

```bash
cuco add agent <name>        # Add an agent
cuco add prompt <name>       # Add a prompt
cuco add skill <name>        # Add a skill
cuco add instructions <name> # Add instructions
cuco list <type>             # List available resources
```

### Custom Sources

```bash
cuco source list                           # List custom sources
cuco source add <name> <type> <url>        # Add a source
cuco source remove <name>                  # Remove a source
```

### Syncing

```bash
cuco sync                    # Sync all resources
cuco sync <name>             # Sync specific resource
```

## Structure

### Project Structure

```
your-project/
└── .github/
    ├── agents/              # Custom agents
    ├── prompts/             # Reusable prompts
    ├── skills/              # Skills
    ├── instructions/        # Instructions
    └── copilot-instructions.md
```

### Package Structure

```
custom_copilot/
├── agents/                  # Public agents
├── prompts/                 # Public prompts
├── skills/                  # Public skills
├── bundles/                 # Pre-configured bundles
└── templates/               # Templates for creating resources
```

## Bundles

Bundles are pre-configured combinations of customizations. The manifest uses these resource types:

- **`custom-copilot`** - Resources from the public custom-copilot repository
- **`bundle`** - Resources included within the bundle
- **`github`** - Resources from 3rd party GitHub repositories (future)

### Example Bundle Manifest

```json
{
  "name": "my-bundle",
  "version": "1.0.0",
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
        "name": "custom-prompt",
        "type": "bundle",
        "path": "prompts/custom.prompt.md"
      }
    ]
  }
}
```

## Private Customizations

Add your company's private customizations repository:

```bash
# Add a private source
cuco source add company git https://github.com/mycompany/copilot-customs.git

# Configuration is stored in ~/.cuco/config.json
# Or use .cuco-config.json in your project for project-specific sources
```

### Configuration File

```json
{
  "sources": [
    {
      "name": "company-internal",
      "type": "git",
      "url": "https://github.com/mycompany/copilot-customs.git"
    }
  ]
}
```

## Creating Custom Resources

### Using Templates

```bash
# Copy agent template
cp custom_copilot/templates/agent-template.agent.md custom_copilot/agents/my-agent.agent.md

# Copy skill template
cp -r custom_copilot/templates/skill-template custom_copilot/skills/my-skill

# Copy bundle template
cp -r custom_copilot/templates/bundle-template custom_copilot/bundles/my-bundle
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Links

- [GitHub Repository](https://github.com/DJ2695/custom-copilot)
- [Issue Tracker](https://github.com/DJ2695/custom-copilot/issues)

---

Made with ❤️ for GitHub Copilot users
