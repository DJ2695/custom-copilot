# Custom Copilot CLI (`cuco`)

A language-agnostic CLI tool for managing GitHub Copilot customizations in any project. The `cuco` tool helps you initialize, add, and sync GitHub Copilot artifacts including agents, prompts, instructions, skills, and MCP servers.

## 📋 Requirements

- Python 3.12 or higher
- pip or [uv](https://github.com/astral-sh/uv) (Python package installers)
- Git (for installation from repository)

## 🚀 Installation

> **📖 For detailed installation instructions, troubleshooting, and platform-specific notes, see [INSTALL.md](INSTALL.md)**

### Option 1: Install from GitHub (Public Repository)

When the repository is public, you can install directly using pip or uv:

#### Using pip

```bash
# Install the latest version from the main branch
pip install git+https://github.com/DJ2695/custom-copilot.git

# Install from a specific branch
pip install git+https://github.com/DJ2695/custom-copilot.git@your-branch-name

# Install from a specific tag/release
pip install git+https://github.com/DJ2695/custom-copilot.git@v0.1.0
```

#### Using uv (Fast Python package installer)

```bash
# Install globally with uv
uv tool install git+https://github.com/DJ2695/custom-copilot.git

# Add to a specific project (creates/updates pyproject.toml)
uv add git+https://github.com/DJ2695/custom-copilot.git

# Add as a dev dependency to your project
uv add --dev git+https://github.com/DJ2695/custom-copilot.git
```

### Option 2: Install from Private GitHub Repository

If you have access to a private repository, use one of these methods:

#### Using SSH (Recommended for private repos)

**With pip:**
```bash
# First, ensure your SSH key is added to your GitHub account
# Then install using SSH URL
pip install git+ssh://git@github.com/DJ2695/custom-copilot.git
```

**With uv:**
```bash
# Install globally
uv tool install git+ssh://git@github.com/DJ2695/custom-copilot.git

# Add to project
uv add git+ssh://git@github.com/DJ2695/custom-copilot.git
```

#### Using Personal Access Token (PAT)

**With pip:**
```bash
# Create a Personal Access Token (PAT) at:
# https://github.com/settings/tokens
# With 'repo' scope for private repositories

# Install using PAT (replace YOUR_TOKEN with your actual token)
pip install git+https://YOUR_TOKEN@github.com/DJ2695/custom-copilot.git

# Or set it as an environment variable for better security
export GITHUB_TOKEN=your_token_here
pip install git+https://${GITHUB_TOKEN}@github.com/DJ2695/custom-copilot.git
```

**With uv:**
```bash
# Set token as environment variable
export GITHUB_TOKEN=your_token_here

# Install globally
uv tool install git+https://${GITHUB_TOKEN}@github.com/DJ2695/custom-copilot.git

# Add to project
uv add git+https://${GITHUB_TOKEN}@github.com/DJ2695/custom-copilot.git
```

### Option 3: Install from Local Source (Development)

For development or if you've cloned the repository:

#### Using pip

```bash
# Clone the repository
git clone https://github.com/DJ2695/custom-copilot.git
cd custom-copilot

# Install in editable mode (changes reflect immediately)
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"
```

#### Using uv

```bash
# Clone the repository
git clone https://github.com/DJ2695/custom-copilot.git
cd custom-copilot

# Install in editable mode
uv pip install -e .

# Or use uv sync (recommended for development)
uv sync

# Install with dev dependencies
uv pip install -e ".[dev]"
```

### Verify Installation

After installation, verify the `cuco` command is available:

```bash
# Check if cuco is installed
cuco help

# If installed with uv tool, it's automatically in PATH
# If using project install, activate your environment first
```

## 🚀 Quick Start

### Initialize a Project

```bash
# Create .github folder structure
cd your-project
cuco init
```

This creates:
```
your-project/
└── .github/
    ├── agents/
    ├── prompts/
    ├── instructions/
    ├── skills/
    └── copilot-instructions.md
```

### List Available Artifacts

```bash
# List available artifacts in the registry
cuco list skills
cuco list prompts
cuco list agents
cuco list mcps
```

### Add Artifacts

```bash
# Add an agent
cuco add agent skill-builder

# Add a prompt
cuco add prompt git

# Add instructions
cuco add instructions sample

# Add a skill
cuco add skill test-driven-development

# Add an MCP server (automatically handles .env setup)
cuco add mcp context7
```

### Sync Artifacts

Keep your artifacts up to date with the registry:

```bash
# Sync all tracked artifacts
cuco sync

# Sync a specific artifact
cuco sync test-driven-development
```

If you've made local modifications, `cuco sync` will prompt you to:
- Overwrite with the registry version
- Keep your local changes

## 📖 Commands

### `cuco init`

Initialize the `.github` folder structure in your project.

**Usage:**
```bash
cuco init
```

**What it does:**
- Creates `.github/` directory (if not exists)
- Creates subdirectories: `agents/`, `prompts/`, `instructions/`, `skills/`
- Creates empty `copilot-instructions.md` file

### `cuco add <type> <name>`

Add an artifact from the package registry to your project.

**Usage:**
```bash
cuco add agent <name>
cuco add prompt <name>
cuco add instructions <name>
cuco add skill <name>
cuco add mcp <name>
```

**Examples:**
```bash
cuco add agent skill-builder
cuco add prompt git
cuco add skill test-driven-development
cuco add mcp context7
```

**What it does:**
- Copies the artifact from the package registry to `.github/<type>/`
- Tracks the artifact in `.github/.cuco-tracking.json`
- Prompts for confirmation if artifact already exists
- **For MCPs**: 
  - Adds MCP server configuration to `.vscode/mcp.json`
  - Detects environment variables (e.g., `${env:API_KEY}`)
  - Creates/updates `.env` file with required variables
  - Prompts you to set the values

### `cuco list <type>`

List available artifacts in the package registry.

**Usage:**
```bash
cuco list agents
cuco list prompts
cuco list instructions
cuco list skills
cuco list mcps
```

**Examples:**
```bash
cuco list skills
# Output:
# Available skills:
#   - skill-creator
#   - systematic-debugging
#   - test-driven-development
#   ...

cuco list mcps
# Output:
# Available mcps:
#   - context7
#   - serena
#   - sequential-thinking
#   ...
```

**What it does:**
- Shows all available artifacts of the specified type from the registry
- Helps you discover what's available before adding

### `cuco sync [artifact-name]`

Sync artifacts with the package registry.

**Usage:**
```bash
# Sync all tracked artifacts
cuco sync

# Sync specific artifact
cuco sync <artifact-name>
```

**Examples:**
```bash
cuco sync                          # Sync everything
cuco sync test-driven-development  # Sync specific skill
```

**What it does:**
- Checks if registry version differs from tracked version
- Detects local modifications using file hashing
- Prompts user if local modifications exist:
  - Option 1: Overwrite with registry version
  - Option 2: Keep local version
- Updates tracking metadata after sync

## 🏗️ Architecture

### Project Structure

```
src/cc/
├── __init__.py           # Package initialization
├── __main__.py           # Entry point for python -m cc
├── cli.py                # Main CLI router
├── utils.py              # Utilities (hashing, tracking)
├── commands/             # Command implementations
│   ├── __init__.py
│   ├── init.py          # cuco init command
│   ├── add.py           # cuco add command
│   └── sync.py          # cuco sync command
└── registry/             # Bundled artifacts
    ├── agents/
    ├── prompts/
    ├── instructions/
    └── skills/
```

### Tracking System

The tool tracks artifacts in `.github/.cuco-tracking.json`:

```json
{
  "artifacts": {
    "skills/test-driven-development": {
      "type": "skills",
      "name": "test-driven-development",
      "source_hash": "abc123...",
      "version": "latest",
      "from_registry": true
    }
  }
}
```

This enables:
- ✅ Detection of local modifications (by comparing hashes)
- ✅ Identification of registry-based vs user-created artifacts
- ✅ Version tracking (future enhancement)
- ✅ Selective sync operations

### How It Works

1. **Registry**: Artifacts are bundled with the package in `src/cc/registry/`
2. **Tracking**: When you `cuco add` an artifact, its hash is stored
3. **Sync Detection**:
   - Compare current file hash with tracked hash → detects local changes
   - Compare tracked hash with registry hash → detects upstream updates
4. **Conflict Resolution**: User prompted to choose between local and registry version

## 🔧 For Contributors

### Adding New Artifacts to Registry

To add a new artifact to the registry:

1. Place the artifact in `src/cc/registry/<type>/`
2. For files: `<name>.md`, `<name>.agent.md`, `<name>.prompt.md`
3. For skills: Create directory `<name>/` with `SKILL.md`

Example:
```bash
# Add a new prompt
cp my-custom-prompt.md src/cc/registry/prompts/

# Add a new skill
cp -r my-skill/ src/cc/registry/skills/
```

### Extending Commands

To add a new command:

1. Create `src/cc/commands/yourcommand.py`
2. Implement `run(args: List[str]) -> int` function
3. Import and route in `src/cc/cli.py`

Example:
```python
# src/cc/commands/yourcommand.py
def run(args: List[str]) -> int:
    print("Your command logic here")
    return 0
```

```python
# src/cc/cli.py
from cc.commands import yourcommand

def main(args):
    # ...
    elif command == "yourcommand":
        return yourcommand.run(args[1:])
```

### Code Guidelines

- **Modular**: Each command is self-contained in its own module
- **Minimal dependencies**: Only Python standard library
- **Clear separation**: CLI routing, command logic, and utilities are separate
- **Type hints**: Use type hints for better code maintainability
- **Documentation**: Docstrings for all public functions

### Testing Your Changes

```bash
# Install in development mode
pip install -e .

# Test commands
cd /tmp/test-project
cuco init
cuco add skill test-driven-development
cuco sync
```

## 🔮 Future Enhancements

- [ ] Remote registry support (fetch from GitHub, npm, etc.)
- [ ] Version pinning and rollback
- [ ] Three-way merge support for conflicts
- [ ] Diff visualization for local modifications
- [ ] Template variables for artifact customization
- [ ] Artifact dependencies and installation order
- [ ] Search registry command (with filters and keywords)
- [ ] Export/share custom artifacts

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2026 DJ2695

## 🤝 Contributing

**Important:** This repository is currently maintained exclusively by [@DJ2695](https://github.com/DJ2695).

At this time, **external contributions are not being accepted**. This includes:
- Pull requests
- Feature requests  
- Bug reports

For more details, please see [CONTRIBUTING.md](CONTRIBUTING.md).

### For Users

If you'd like to customize this tool for your needs:
- ✅ Fork this repository
- ✅ Modify it according to the MIT License
- ✅ Create your own version

### For the Repository Owner

Development workflow:
```bash
# Clone and install in editable mode
git clone https://github.com/DJ2695/custom-copilot.git
cd custom-copilot
pip install -e .

# Make changes and test
cuco help
```

---

**Note**: This tool is language-agnostic and works with any project type. The `.github` customizations work with GitHub Copilot regardless of your project's programming language.