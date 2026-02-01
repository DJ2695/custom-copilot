# Custom Copilot CLI (`cc`)

A language-agnostic CLI tool for managing GitHub Copilot customizations in any project. The `cc` tool helps you initialize, add, and sync GitHub Copilot artifacts including agents, prompts, instructions, skills, and MCP servers.

## 🚀 Quick Start

### Installation

```bash
# Install from source
pip install -e .

# The 'cc' command will now be available globally
cc help
```

### Initialize a Project

```bash
# Create .github folder structure
cd your-project
cc init
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
cc list skills
cc list prompts
cc list agents
cc list mcps
```

### Add Artifacts

```bash
# Add an agent
cc add agent skill-builder

# Add a prompt
cc add prompt git

# Add instructions
cc add instructions sample

# Add a skill
cc add skill test-driven-development

# Add an MCP server (automatically handles .env setup)
cc add mcp context7
```

### Sync Artifacts

Keep your artifacts up to date with the registry:

```bash
# Sync all tracked artifacts
cc sync

# Sync a specific artifact
cc sync test-driven-development
```

If you've made local modifications, `cc sync` will prompt you to:
- Overwrite with the registry version
- Keep your local changes

## 📖 Commands

### `cc init`

Initialize the `.github` folder structure in your project.

**Usage:**
```bash
cc init
```

**What it does:**
- Creates `.github/` directory (if not exists)
- Creates subdirectories: `agents/`, `prompts/`, `instructions/`, `skills/`
- Creates empty `copilot-instructions.md` file

### `cc add <type> <name>`

Add an artifact from the package registry to your project.

**Usage:**
```bash
cc add agent <name>
cc add prompt <name>
cc add instructions <name>
cc add skill <name>
cc add mcp <name>
```

**Examples:**
```bash
cc add agent skill-builder
cc add prompt git
cc add skill test-driven-development
cc add mcp context7
```

**What it does:**
- Copies the artifact from the package registry to `.github/<type>/`
- Tracks the artifact in `.github/.cc-tracking.json`
- Prompts for confirmation if artifact already exists
- **For MCPs**: 
  - Adds MCP server configuration to `.vscode/mcp.json`
  - Detects environment variables (e.g., `${env:API_KEY}`)
  - Creates/updates `.env` file with required variables
  - Prompts you to set the values

### `cc list <type>`

List available artifacts in the package registry.

**Usage:**
```bash
cc list agents
cc list prompts
cc list instructions
cc list skills
cc list mcps
```

**Examples:**
```bash
cc list skills
# Output:
# Available skills:
#   - skill-creator
#   - systematic-debugging
#   - test-driven-development
#   ...

cc list mcps
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

### `cc sync [artifact-name]`

Sync artifacts with the package registry.

**Usage:**
```bash
# Sync all tracked artifacts
cc sync

# Sync specific artifact
cc sync <artifact-name>
```

**Examples:**
```bash
cc sync                          # Sync everything
cc sync test-driven-development  # Sync specific skill
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
│   ├── init.py          # cc init command
│   ├── add.py           # cc add command
│   └── sync.py          # cc sync command
└── registry/             # Bundled artifacts
    ├── agents/
    ├── prompts/
    ├── instructions/
    └── skills/
```

### Tracking System

The tool tracks artifacts in `.github/.cc-tracking.json`:

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
2. **Tracking**: When you `cc add` an artifact, its hash is stored
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
cc init
cc add skill test-driven-development
cc sync
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

This project is part of the DJ2695/custom-copilot repository.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new artifacts to the registry
- Improve conflict resolution logic
- Enhance CLI user experience
- Add new commands
- Improve documentation

---

**Note**: This tool is language-agnostic and works with any project type. The `.github` customizations work with GitHub Copilot regardless of your project's programming language.