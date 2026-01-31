# Workflow Patterns Reference

## Reusable Workflows

### Caller Workflow

```yaml
# .github/workflows/deploy-staging.yaml
jobs:
  deploy:
    uses: ./.github/workflows/reusable-deploy.yaml
    with:
      environment: staging
    secrets:
      deploy-token: ${{ secrets.STAGING_TOKEN }}
```

### Reusable Workflow

```yaml
# .github/workflows/reusable-deploy.yaml
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      deploy-token:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - uses: actions/checkout@v4
      - name: Deploy
        run: ./deploy.sh ${{ inputs.environment }}
        env:
          TOKEN: ${{ secrets.deploy-token }}
```

## Conditional Execution

### Based on Branch

```yaml
steps:
  - name: Run only on main
    if: github.ref == 'refs/heads/main'
    run: echo "Main branch"
  
  - name: Run on PR
    if: github.event_name == 'pull_request'
    run: echo "Pull request"
```

### Based on Previous Step

```yaml
steps:
  - name: Build
    id: build
    run: npm run build
  
  - name: Deploy only if build succeeded
    if: success()
    run: ./deploy.sh
  
  - name: Notify on failure
    if: failure()
    run: ./notify-failure.sh
```

### Based on Files Changed

```yaml
on:
  push:
    paths:
      - 'src/**'
      - 'package.json'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Build affected code
        run: npm run build
```

## Caching Strategies

### NPM Dependencies

```yaml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'

- run: npm ci
```

### Custom Cache

```yaml
- name: Cache dependencies
  uses: actions/cache@v4
  with:
    path: |
      ~/.npm
      node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

## Artifacts

### Upload

```yaml
- name: Build
  run: npm run build

- name: Upload build artifacts
  uses: actions/upload-artifact@v4
  with:
    name: build-files
    path: dist/
    retention-days: 7
```

### Download in Another Job

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/
      - run: ./deploy.sh
```

## Concurrency Control

### Cancel In-Progress Runs

```yaml
name: Deploy

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

on:
  push:
    branches: [main]
```

### Queue Sequential Deployments

```yaml
concurrency:
  group: production-deploy
  cancel-in-progress: false  # Queue instead of cancel
```

## Environment Variables

### Workflow Level

```yaml
env:
  NODE_ENV: production
  API_URL: https://api.example.com

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: echo $NODE_ENV
```

### Job Level

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    env:
      DEPLOY_ENV: staging
    steps:
      - run: echo $DEPLOY_ENV
```

### Step Level

```yaml
steps:
  - name: Deploy
    run: ./deploy.sh
    env:
      API_KEY: ${{ secrets.API_KEY }}
```

## Composite Actions

Create reusable action steps:

```yaml
# .github/actions/setup-app/action.yaml
name: 'Setup App'
description: 'Setup Node.js and install dependencies'

runs:
  using: 'composite'
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'
    - run: npm ci
      shell: bash
```

**Use in workflow:**
```yaml
steps:
  - uses: actions/checkout@v4
  - uses: ./.github/actions/setup-app
  - run: npm test
```

## Matrix Strategy

### Basic Matrix

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest]
    node: [18, 20]
```

### Include Additional Combinations

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest]
    node: [18, 20]
    include:
      - os: windows-latest
        node: 20
```

### Exclude Combinations

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
    node: [18, 20]
    exclude:
      - os: macos-latest
        node: 18
```

## Scheduled Workflows

```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
    - cron: '0 0 * * 0'  # Weekly on Sunday

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - run: ./cleanup.sh
```

## Notification Patterns

### Slack Notification

```yaml
- name: Notify Slack on failure
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "❌ Deployment failed: ${{ github.event.head_commit.message }}",
        "username": "GitHub Actions"
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### Create GitHub Issue on Failure

```yaml
- name: Create issue on failure
  if: failure()
  uses: actions/github-script@v7
  with:
    script: |
      github.rest.issues.create({
        owner: context.repo.owner,
        repo: context.repo.repo,
        title: 'Workflow failed: ${{ github.workflow }}',
        body: 'Run: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}'
      })
```

## Permissions

### Restrict Default Permissions

```yaml
permissions:
  contents: read
  pull-requests: write

jobs:
  pr-comment:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: 'PR validated!'
            })
```
