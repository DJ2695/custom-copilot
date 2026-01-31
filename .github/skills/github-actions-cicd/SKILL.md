---
name: github-actions-cicd
description: 'Create and manage GitHub Actions workflows for CI/CD pipelines. Use when: (1) Creating new workflow files, (2) Setting up PR checks and automated testing, (3) Configuring deployment pipelines, (4) Managing secrets and environment variables, (5) Debugging workflow failures, (6) Setting up manual triggers or approvals, or working with .github/workflows. Keywords: github actions, ci/cd, workflow, pipeline, deployment, automation, pr checks, continuous integration.'
---

# GitHub Actions CI/CD

Create and manage GitHub Actions workflows for continuous integration, testing, and deployment pipelines.

## When to Use This Skill

- Creating new workflow files in `.github/workflows/`
- Setting up PR validation and automated testing
- Configuring deployment pipelines (staging/production)
- Managing GitHub secrets and environment variables
- Debugging workflow failures
- Setting up manual workflow triggers or deployment approvals

## Prerequisites

**Required:** GitHub repository with Actions enabled

**Tools:** [GitHub CLI](https://cli.github.com/) (`gh`), [act](https://github.com/nektos/act) (optional, for local testing)

## Workflow Basics

**Location:** `.github/workflows/<name>.yaml`

**Structure:**
```yaml
name: Workflow Name
on: [push, pull_request]
jobs:
  job-name:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "Hello"
```

## Common Patterns

### PR Validation
```yaml
on: pull_request
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm test
```

### Environment Deployments
```yaml
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production  # Requires approval
    steps:
      - uses: actions/checkout@v4
      - run: ./deploy.sh
```

### Manual Triggers
```yaml
on: workflow_dispatch  # Shows "Run workflow" button
```

## Secrets Management

**Add:** Repository Settings → Secrets → New secret

**Use:**
```yaml
env:
  API_KEY: ${{ secrets.API_KEY }}
```

## Debugging

```bash
gh run list            # List runs
gh run view <id>       # View details
gh run watch           # Watch real-time
gh run rerun <id>      # Retry failed run
```

## Templates & References

- **[PR Checks Template](templates/pr-checks.yaml)** - Lint and test validation
- **[Multi-Environment Deploy](templates/multi-env-deploy.yaml)** - Staging/production pipeline
- **[Production with Approval](templates/production-approval.yaml)** - Manual approval workflow
- **[Matrix Testing](templates/matrix-testing.yaml)** - Test across versions/platforms
- **[Workflow Patterns](references/workflow-patterns.md)** - Advanced configurations
- **[Triggers Reference](references/triggers.md)** - All trigger types and options
- **[Troubleshooting](references/troubleshooting.md)** - Common issues and solutions

## Best Practices

✅ Pin action versions (`@v4`), cache dependencies, use environments for production
❌ Never hardcode secrets, don't use `pull_request_target` without understanding risks

## Quick Reference

```bash
# Workflows
gh workflow list
gh workflow run <name>

# Runs
gh run list
gh run view <id>
gh run cancel <id>

# Secrets
gh secret set NAME
gh secret list
```

## Common Actions

- `actions/checkout@v4` - Clone repository
- `actions/setup-node@v4` - Setup Node.js
- `actions/cache@v4` - Cache dependencies
- `actions/upload-artifact@v4` - Save files
