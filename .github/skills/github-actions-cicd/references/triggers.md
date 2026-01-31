# Triggers Reference

## Event Types

### Push

Trigger on commits to branches:

```yaml
on:
  push:
    branches:
      - main
      - 'release/**'
    tags:
      - 'v*'
    paths:
      - 'src/**'
      - '**.js'
```

### Pull Request

```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened]
    branches:
      - main
    paths-ignore:
      - '**.md'
      - 'docs/**'
```

**Types:**
- `opened` - PR created
- `synchronize` - New commits pushed
- `reopened` - Closed PR reopened
- `closed` - PR closed/merged
- `ready_for_review` - Draft converted to ready

### Workflow Dispatch

Manual trigger with inputs:

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        type: choice
        options:
          - staging
          - production
      dry-run:
        description: 'Dry run mode'
        required: false
        type: boolean
        default: false

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying to ${{ inputs.environment }}"
      - run: |
          if [ "${{ inputs.dry-run }}" == "true" ]; then
            echo "Dry run mode"
          fi
```

### Schedule

Cron-based scheduling:

```yaml
on:
  schedule:
    - cron: '0 2 * * *'      # Daily at 2 AM UTC
    - cron: '0 0 * * 0'      # Sunday midnight
    - cron: '*/15 * * * *'   # Every 15 minutes
```

**Cron format:** `minute hour day month weekday`

### Release

```yaml
on:
  release:
    types: [published, created, released]
```

### Workflow Call

For reusable workflows:

```yaml
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      version:
        required: false
        type: string
        default: 'latest'
    secrets:
      token:
        required: true
```

## Multiple Triggers

```yaml
on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:
  schedule:
    - cron: '0 2 * * *'
```

## Path Filtering

### Include Paths

```yaml
on:
  push:
    paths:
      - 'src/**'
      - 'lib/**'
      - 'package.json'
      - '**.js'
```

### Exclude Paths

```yaml
on:
  push:
    paths-ignore:
      - '**.md'
      - 'docs/**'
      - '.gitignore'
```

**Note:** Cannot use both `paths` and `paths-ignore` together

## Branch Filtering

### Include Branches

```yaml
on:
  push:
    branches:
      - main
      - develop
      - 'release/**'    # Wildcard pattern
      - 'feature/*'
```

### Exclude Branches

```yaml
on:
  push:
    branches-ignore:
      - 'wip/**'
      - 'experimental/**'
```

## Tag Filtering

```yaml
on:
  push:
    tags:
      - 'v*'           # v1, v2, v1.0.0
      - 'v[0-9]+.*'    # v1.0, v2.5
      - '!v*-alpha'    # Exclude alpha tags
```

## Activity Types by Event

### Issues

```yaml
on:
  issues:
    types: [opened, edited, deleted, closed, reopened, labeled]
```

### Issue Comment

```yaml
on:
  issue_comment:
    types: [created, edited, deleted]
```

### Pull Request Review

```yaml
on:
  pull_request_review:
    types: [submitted, edited, dismissed]
```

### Pull Request Target

**⚠️ Security Warning:** Has write access to base branch. Use carefully.

```yaml
on:
  pull_request_target:
    types: [opened, synchronize]
```

**Safe pattern:**
```yaml
jobs:
  comment:
    runs-on: ubuntu-latest
    steps:
      # Don't checkout PR code
      - uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({...})
```

## Workflow Run

Trigger on completion of another workflow:

```yaml
on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    steps:
      - run: echo "CI passed, deploying..."
```

## Repository Dispatch

Trigger via API:

```yaml
on:
  repository_dispatch:
    types: [deploy-command]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Client payload: ${{ toJson(github.event.client_payload) }}"
```

**Trigger via API:**
```bash
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/OWNER/REPO/dispatches \
  -d '{"event_type":"deploy-command","client_payload":{"env":"production"}}'
```

## Webhook Events

Less common but available:

- `check_run` - Check run created/updated
- `check_suite` - Check suite completed
- `create` - Branch/tag created
- `delete` - Branch/tag deleted
- `deployment` - Deployment created
- `fork` - Repository forked
- `gollum` - Wiki page updated
- `label` - Label created/updated
- `milestone` - Milestone created/updated
- `page_build` - GitHub Pages build
- `project` - Project board event
- `registry_package` - Package published
- `status` - Commit status updated
- `watch` - Repository starred

## Best Practices

✅ **DO:**
- Use path filters to avoid unnecessary runs
- Use `pull_request` (not `pull_request_target`) when possible
- Combine related triggers
- Use `workflow_dispatch` for debugging

❌ **DON'T:**
- Over-trigger (e.g., run on every file change)
- Use `pull_request_target` without understanding security
- Schedule workflows too frequently (respect GitHub limits)
- Trigger on `push` to all branches if not needed
