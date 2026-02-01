# Git Repository Support - Implementation Guide

## Overview

Custom Copilot now supports private git repositories for company-internal customizations. This allows organizations to maintain their own customizations separate from the public repository.

## Quick Start

### 1. Set Up Your Private Repository

Create a git repository with this structure:

```
mycompany/copilot-customs/
└── custom_copilot/
    ├── agents/
    │   └── company-agent.agent.md
    ├── prompts/
    │   └── company-prompt.prompt.md
    ├── skills/
    │   └── company-skill/
    │       └── SKILL.md
    └── bundles/
        └── company-bundle/
            └── bundle.json
```

**Important:** The repository must contain a `custom_copilot/` folder at the root.

### 2. Add the Repository as a Source

```bash
# Using HTTPS
cuco source add my-company https://github.com/mycompany/copilot-customs.git

# Using SSH (recommended for private repos)
cuco source add my-company git@github.com:mycompany/copilot-customs.git

# Verify
cuco source list
```

### 3. Use in Bundles

Create or update a bundle to reference your custom resources:

```json
{
  "name": "company-bundle",
  "version": "1.0.0",
  "dependencies": {
    "agents": [
      {
        "name": "company-agent",
        "type": "custom",
        "source_name": "my-company",
        "source": "agents/company-agent.agent.md"
      }
    ],
    "skills": [
      {
        "name": "public-skill",
        "type": "custom-copilot",
        "source": "skills/test-driven-development"
      }
    ]
  }
}
```

## Resource Types

| Type | Description | Fields Required |
|------|-------------|-----------------|
| `bundle` | Resources within the bundle itself | `path` |
| `custom-copilot` | Resources from the public repository | `source` |
| `custom` | Resources from a configured git source | `source_name`, `source` |
| `github` | Resources from 3rd party repos (future) | `url` |

## Authentication

### HTTPS URLs

**Setup:**
1. Configure git credential helper
2. Or use a personal access token

**Authentication Flow:**
- Git will prompt for credentials on first clone
- Credentials are cached by git credential helper
- Subsequent operations use cached credentials

**Example:**
```bash
# Configure credential helper (one time)
git config --global credential.helper store

# Add source
cuco source add my-company https://github.com/mycompany/copilot-customs.git

# First use will prompt for credentials
cuco bundle add company-bundle
```

### SSH URLs

**Setup:**
1. Generate SSH key: `ssh-keygen -t rsa -b 4096`
2. Add to ssh-agent: `ssh-add ~/.ssh/id_rsa`
3. Add public key to GitHub/GitLab

**Authentication Flow:**
- No password prompts
- Uses SSH keys from ssh-agent
- Faster and more secure

**Example:**
```bash
# Add SSH key to agent
ssh-add ~/.ssh/id_rsa

# Add source with SSH URL
cuco source add my-company git@github.com:mycompany/copilot-customs.git

# No authentication prompts
cuco bundle add company-bundle
```

## How It Works

### Repository Caching

When you reference a custom source:

1. **First Access:**
   - Repository is cloned to `~/.cuco/repos/<source-name>/`
   - The `custom_copilot/` folder is located
   - Resources are copied from there

2. **Subsequent Access:**
   - Repository is updated with `git pull`
   - If update fails, uses existing cached version
   - Resources are copied from updated repo

### Directory Structure

```
~/.cuco/
├── config.json                    # Configuration
└── repos/                         # Cached repositories
    ├── my-company/                # Git repo cache
    │   └── custom_copilot/        # Resources here
    │       ├── agents/
    │       ├── prompts/
    │       └── skills/
    └── another-source/
        └── custom_copilot/
```

## Configuration

### Global Configuration

Located at `~/.cuco/config.json`:

```json
{
  "sources": [
    {
      "name": "my-company",
      "type": "git",
      "url": "git@github.com:mycompany/copilot-customs.git"
    },
    {
      "name": "partner-org",
      "type": "git",
      "url": "https://github.com/partner/copilot-customs.git"
    }
  ]
}
```

### Project-Specific Configuration

Create `.cuco-config.json` in your project root for project-specific sources:

```json
{
  "sources": [
    {
      "name": "project-specific",
      "type": "git",
      "url": "git@github.com:myorg/project-customs.git"
    }
  ]
}
```

Project-specific configuration takes precedence over global.

## Examples

### Example 1: Company-Wide Standards

**Repository:** `mycompany/copilot-standards`

```
custom_copilot/
├── agents/
│   └── code-reviewer.agent.md
├── skills/
│   └── company-style-guide/
│       └── SKILL.md
└── bundles/
    └── company-standards/
        └── bundle.json
```

**Setup:**
```bash
cuco source add company git@github.com:mycompany/copilot-standards.git
cuco bundle add company-standards
```

### Example 2: Department-Specific Tools

**Repository:** `mycompany/data-science-tools`

```
custom_copilot/
├── agents/
│   └── ml-optimizer.agent.md
├── prompts/
│   └── data-analysis.prompt.md
└── skills/
    └── statistical-validation/
        └── SKILL.md
```

**Bundle using multiple sources:**
```json
{
  "name": "data-science-bundle",
  "dependencies": {
    "agents": [
      {
        "type": "custom",
        "source_name": "company",
        "source": "agents/code-reviewer.agent.md"
      },
      {
        "type": "custom",
        "source_name": "data-science",
        "source": "agents/ml-optimizer.agent.md"
      }
    ],
    "skills": [
      {
        "type": "custom-copilot",
        "source": "skills/test-driven-development"
      }
    ]
  }
}
```

### Example 3: Mixed Public and Private

Combine public and private resources:

```json
{
  "name": "enterprise-bundle",
  "dependencies": {
    "agents": [
      {
        "name": "public-skill-builder",
        "type": "custom-copilot",
        "source": "agents/skill-builder.agent.md"
      },
      {
        "name": "company-reviewer",
        "type": "custom",
        "source_name": "company",
        "source": "agents/code-reviewer.agent.md"
      }
    ],
    "skills": [
      {
        "name": "tdd",
        "type": "custom-copilot",
        "source": "skills/test-driven-development"
      },
      {
        "name": "company-standards",
        "type": "custom",
        "source_name": "company",
        "source": "skills/company-style-guide"
      }
    ]
  }
}
```

## Troubleshooting

### Authentication Errors

**Problem:** `Failed to clone repository: authentication failed`

**Solutions:**
1. **HTTPS:** Set up git credential helper or use personal access token
2. **SSH:** Add your SSH key to ssh-agent: `ssh-add ~/.ssh/id_rsa`
3. Verify you have access to the repository

### Repository Not Found

**Problem:** `Repository does not have a custom_copilot folder`

**Solution:** Ensure your repository has the correct structure:
```
your-repo/
└── custom_copilot/     # Must be at root level
    ├── agents/
    ├── prompts/
    └── skills/
```

### Update Failures

**Problem:** `Failed to update repository`

**Solution:** The tool will use the cached version. Check:
1. Your internet connection
2. Repository access permissions
3. Git credentials are still valid

### Slow Cloning

**Problem:** Initial clone takes a long time

**Solutions:**
1. Use SSH instead of HTTPS
2. Check network connection
3. Repository will be cached, subsequent access is fast

## Best Practices

### 1. Use SSH for Private Repositories

SSH is faster and doesn't require password prompts:
```bash
cuco source add company git@github.com:mycompany/copilot-customs.git
```

### 2. Organize by Scope

- Company-wide: One source for all company customizations
- Department: Separate sources for specialized needs
- Project: Use `.cuco-config.json` for project-specific sources

### 3. Version Your Bundles

Include version in bundle names:
```
bundles/
├── company-standards-v1/
└── company-standards-v2/
```

### 4. Document Dependencies

In bundle descriptions, explain what each resource does:
```json
{
  "agents": [{
    "name": "code-reviewer",
    "type": "custom",
    "source_name": "company",
    "source": "agents/code-reviewer.agent.md",
    "description": "Enforces company coding standards and best practices"
  }]
}
```

### 5. Test Before Sharing

Test bundles locally before sharing with your team:
```bash
cuco init
cuco bundle add my-new-bundle
# Verify everything works
```

## Security Considerations

### Private Repositories

- Use SSH keys for authentication
- Rotate SSH keys regularly
- Use repository access controls
- Keep sensitive data out of bundles

### Credentials

- Never commit credentials to git
- Use git credential helper for HTTPS
- Use ssh-agent for SSH keys
- Consider using SSH key passphrases

### Access Control

- Limit repository access to authorized users
- Use organization/team-based permissions
- Audit repository access regularly
- Remove access when team members leave

## Support

For issues or questions:
- Check troubleshooting section above
- Review error messages carefully
- Test with a public repository first
- Check git authentication separately: `git clone <url>`

---

**Version:** 0.3.0  
**Last Updated:** 2026-02-01
