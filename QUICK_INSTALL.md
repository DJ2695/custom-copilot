# Quick Installation Reference

## TL;DR - Installation Commands

### Public Repository

#### Using pip (Global)
```bash
pip install git+https://github.com/DJ2695/custom-copilot.git
```

#### Using uv (Global - Recommended)
```bash
# Install as global tool (automatically in PATH)
uv tool install git+https://github.com/DJ2695/custom-copilot.git
```

#### Using uv (Project-specific)
```bash
# Navigate to your project first
cd /path/to/your/project

# Add as dev dependency (recommended for tools)
uv add --dev git+https://github.com/DJ2695/custom-copilot.git

# Then use with:
uv run cuco help
```

### Private Repository - SSH

#### Using pip
```bash
pip install git+ssh://git@github.com/DJ2695/custom-copilot.git
```

#### Using uv (Global)
```bash
uv tool install git+ssh://git@github.com/DJ2695/custom-copilot.git
```

#### Using uv (Project-specific)
```bash
# Add to your project
uv add --dev git+ssh://git@github.com/DJ2695/custom-copilot.git
```

### Private Repository - Personal Access Token

#### Using pip
```bash
# Option 1: Direct (less secure, token visible in history)
pip install git+https://YOUR_TOKEN@github.com/DJ2695/custom-copilot.git

# Option 2: Environment variable (recommended)
export GITHUB_TOKEN=your_token_here
pip install git+https://${GITHUB_TOKEN}@github.com/DJ2695/custom-copilot.git
```

#### Using uv (Global)
```bash
# Set token as environment variable
export GITHUB_TOKEN=your_token_here

# Install as global tool
uv tool install git+https://${GITHUB_TOKEN}@github.com/DJ2695/custom-copilot.git
```

#### Using uv (Project-specific)
```bash
# Set token as environment variable
export GITHUB_TOKEN=your_token_here

# Add as dev dependency
uv add --dev git+https://${GITHUB_TOKEN}@github.com/DJ2695/custom-copilot.git
```

### Local Development

#### Using pip
```bash
git clone https://github.com/DJ2695/custom-copilot.git
cd custom-copilot
pip install -e .
```

#### Using uv (Recommended)
```bash
git clone https://github.com/DJ2695/custom-copilot.git
cd custom-copilot

# Use uv sync (automatically handles everything)
uv sync

# Then run commands with:
uv run cuco help
```

## Verify Installation

### If installed globally
```bash
cuco help
```

### If installed in project with uv
```bash
uv run cuco help
```

## UV vs PIP: When to Use Which?

### Use `uv tool install` (Global) When:
- ✅ You want the CLI available everywhere
- ✅ You use this tool across multiple projects
- ✅ You want the fastest installation
- ✅ You want automatic PATH management

### Use `uv add --dev` (Project-specific) When:
- ✅ You want different versions per project
- ✅ You want to track dependencies in pyproject.toml
- ✅ You're working in a team and want reproducible environments
- ✅ You want to use `uv run cuco` to ensure correct version

### Use `pip install` When:
- ✅ You don't have uv installed
- ✅ You're in a CI/CD environment
- ✅ You need traditional Python package management

## Quick uv Setup

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install this package globally
uv tool install git+https://github.com/DJ2695/custom-copilot.git

# Use it anywhere
cuco help
```

## Making the Repository Public

To make this repository public while restricting contributions:

1. **On GitHub:**
   - Go to Repository Settings
   - Scroll to "Danger Zone"
   - Click "Change visibility"
   - Select "Make public"
   - Confirm the action

2. **Contribution Restrictions Already in Place:**
   - ✅ CONTRIBUTING.md restricts external contributions
   - ✅ Pull request template warns contributors
   - ✅ Issue templates disabled for external users
   - ✅ README clearly states contribution policy

3. **GitHub Repository Settings (Optional but Recommended):**
   - Settings → General → Features:
     - ✅ Keep Wikis disabled
     - ✅ Keep Projects disabled  
     - ✅ Keep Discussions disabled (unless you want them)
   
   - Settings → Branches:
     - Add branch protection rules for `main`:
       - ✅ Require pull request reviews before merging
       - ✅ Require status checks to pass
       - ✅ Include administrators (so only you can push)
   
   - Settings → Moderation:
     - Set interaction limits if needed

4. **After Making Public:**
   Users can install with:
   ```bash
   pip install git+https://github.com/DJ2695/custom-copilot.git
   ```

## License

The MIT License allows others to:
- ✅ Use the software commercially
- ✅ Modify the software
- ✅ Distribute the software
- ✅ Use the software privately
- ✅ Fork and create their own versions

But they must:
- Include the original license and copyright notice
- Not hold you liable

This means users can fork and modify the code for their own needs, but cannot contribute back to your repository due to the contribution policy.
