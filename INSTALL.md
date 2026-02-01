# Installation Guide

This guide covers all methods for installing the Custom Copilot CLI (`cc`).

## Prerequisites

- **Python**: 3.12 or higher
- **pip**: Latest version recommended (`pip install --upgrade pip`)
- **Git**: Required for installing from repository

## Installation Methods

### 1. Install from GitHub (Public Repository)

When the repository is public, this is the simplest method:

```bash
# Install from main branch
pip install git+https://github.com/DJ2695/custom-copilot.git

# Install from a specific branch
pip install git+https://github.com/DJ2695/custom-copilot.git@feature-branch

# Install from a specific tag/release
pip install git+https://github.com/DJ2695/custom-copilot.git@v0.1.0
```

### 2. Install from Private Repository

If you have access to a private repository, use one of these authentication methods:

#### Option A: SSH Authentication (Recommended)

**Setup:**
1. Generate an SSH key if you don't have one:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
2. Add the SSH key to your GitHub account:
   - Go to GitHub Settings → SSH and GPG keys
   - Click "New SSH key"
   - Paste your public key (`~/.ssh/id_ed25519.pub`)

**Install:**
```bash
pip install git+ssh://git@github.com/DJ2695/custom-copilot.git
```

#### Option B: Personal Access Token (PAT)

**Setup:**
1. Create a Personal Access Token:
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Click "Generate new token (classic)"
   - Select scope: `repo` (for private repositories)
   - Copy the generated token

**Install (Method 1 - Direct):**
```bash
pip install git+https://YOUR_TOKEN@github.com/DJ2695/custom-copilot.git
```

**Install (Method 2 - Environment Variable, More Secure):**
```bash
export GITHUB_TOKEN=your_token_here
pip install git+https://${GITHUB_TOKEN}@github.com/DJ2695/custom-copilot.git
```

**Install (Method 3 - Use .netrc file):**
Create or edit `~/.netrc`:
```
machine github.com
login YOUR_GITHUB_USERNAME
password YOUR_TOKEN
```
Then:
```bash
pip install git+https://github.com/DJ2695/custom-copilot.git
```

### 3. Install from Local Source (Development)

For development or when you have the repository cloned:

```bash
# Clone the repository
git clone https://github.com/DJ2695/custom-copilot.git
# For private repo with SSH:
# git clone git@github.com:DJ2695/custom-copilot.git

cd custom-copilot

# Install in editable mode (recommended for development)
pip install -e .

# Or install normally
pip install .
```

**Editable mode benefits:**
- Changes to the code take effect immediately
- No need to reinstall after modifying files
- Perfect for development and testing

### 4. Install from Wheel File

If you have a pre-built wheel file:

```bash
pip install copilot-0.1.0-py3-none-any.whl
```

## Verification

After installation, verify the CLI is working:

```bash
# Check if cc command is available (should show help)
cc help

# Verify Python can import the package
python -c "import cc; print(cc.__version__)"

# Test basic functionality
cd /tmp/test-project
cc init
cc list skills
```

## Upgrading

To upgrade to the latest version:

```bash
# From public GitHub
pip install --upgrade git+https://github.com/DJ2695/custom-copilot.git

# From private GitHub (SSH)
pip install --upgrade git+ssh://git@github.com/DJ2695/custom-copilot.git

# From local source
cd custom-copilot
git pull
pip install --upgrade -e .
```

## Uninstalling

To remove the package:

```bash
pip uninstall copilot
```

## Troubleshooting

### Issue: "command not found: cc"

**Solution:** The script directory might not be in your PATH.

```bash
# Find where pip installed scripts
python -m site --user-base

# Add to your PATH in ~/.bashrc or ~/.zshrc:
export PATH="$HOME/.local/bin:$PATH"

# Or use Python module directly:
python -m cc help
```

### Issue: Authentication failed for private repository

**Solution:** Verify your credentials:

```bash
# For SSH:
ssh -T git@github.com

# For PAT:
# Ensure the token has 'repo' scope
# Check token hasn't expired
```

### Issue: "No module named 'cc'"

**Solution:** The package isn't installed or isn't in Python's path.

```bash
# Verify installation
pip list | grep copilot

# Reinstall
pip install --force-reinstall git+https://github.com/DJ2695/custom-copilot.git
```

### Issue: SSL certificate errors

**Solution:** Update certificates or temporarily disable verification (not recommended for production):

```bash
# Update pip
pip install --upgrade pip

# If necessary (not recommended):
pip install --trusted-host github.com git+https://github.com/DJ2695/custom-copilot.git
```

## Platform-Specific Notes

### Windows

- Use Command Prompt or PowerShell
- You might need to add Python Scripts to PATH:
  ```
  C:\Users\YourName\AppData\Local\Programs\Python\Python312\Scripts
  ```

### macOS

- If using Homebrew Python, scripts are in `/usr/local/bin`
- You might need to use `pip3` instead of `pip`

### Linux

- Scripts typically installed to `~/.local/bin`
- Ensure this directory is in your PATH

## CI/CD Integration

### GitHub Actions

```yaml
- name: Install Custom Copilot CLI
  run: |
    pip install git+https://${{ secrets.GITHUB_TOKEN }}@github.com/DJ2695/custom-copilot.git
```

### Docker

```dockerfile
FROM python:3.12-slim

RUN pip install git+https://github.com/DJ2695/custom-copilot.git

CMD ["cc", "help"]
```

## Next Steps

After successful installation:
1. Read the [README.md](README.md) for usage examples
2. Try `cc init` in a project directory
3. Explore available artifacts with `cc list skills`

For issues or questions, refer to [CONTRIBUTING.md](CONTRIBUTING.md).
