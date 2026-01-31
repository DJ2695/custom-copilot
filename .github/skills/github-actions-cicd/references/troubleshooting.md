# Troubleshooting GitHub Actions

## Common Issues

### Workflow Not Triggering

| Symptom | Cause | Solution |
|---------|-------|----------|
| Workflow doesn't run on push | Branch name doesn't match trigger | Check `on.push.branches` matches actual branch |
| PR workflow not running | Path filter excludes changed files | Review `paths` and `paths-ignore` |
| Scheduled workflow skipped | Repository inactive >60 days | Push commit or disable/re-enable workflow |
| Manual trigger not visible | `workflow_dispatch` not in default branch | Merge workflow to default branch first |

### Permission Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Resource not accessible by integration` | Insufficient GITHUB_TOKEN permissions | Add `permissions:` key to workflow |
| `refusing to allow...` | Protected branch restrictions | Check branch protection settings |
| Can't write to repository | Read-only token | Set `permissions: contents: write` |
| Can't comment on PR | No PR write permission | Set `permissions: pull-requests: write` |

**Example fix:**
```yaml
permissions:
  contents: write
  pull-requests: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps: [...]
```

### Secret Issues

| Problem | Solution |
|---------|----------|
| Secret not found | Verify secret name matches exactly (case-sensitive) |
| Secret empty in workflow | Check secret is set for correct environment/scope |
| Can't access org secret | Verify org secret allows this repository |
| Secret visible in logs | Never echo secrets; they should be auto-masked |

### Timeout Issues

**Default timeout:** 360 minutes (6 hours)

**Increase timeout:**
```yaml
jobs:
  long-job:
    runs-on: ubuntu-latest
    timeout-minutes: 120
    steps: [...]
```

**Step-level timeout:**
```yaml
steps:
  - name: Long running step
    run: ./long-process.sh
    timeout-minutes: 30
```

### Caching Problems

**Cache not restoring:**
```yaml
- uses: actions/cache@v4
  with:
    path: node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

**Tips:**
- Verify `key` changes when dependencies change
- Use `restore-keys` for partial matches
- Cache size limit: 10 GB per repository
- Caches older than 7 days are deleted

### Artifact Issues

**Artifact not found:**
- Verify artifact name matches exactly
- Check artifact hasn't expired (default: 90 days)
- Ensure upload job completed successfully

**Size limits:**
- Free: 500 MB per artifact
- Teams/Enterprise: 2 GB per artifact

### Matrix Job Failures

**Some combinations fail:**
```yaml
strategy:
  matrix:
    os: [ubuntu, macos, windows]
    node: [18, 20]
  fail-fast: false  # Continue other jobs if one fails
```

**Exclude specific combinations:**
```yaml
strategy:
  matrix:
    os: [ubuntu, macos, windows]
    node: [18, 20]
    exclude:
      - os: macos
        node: 18
```

## Debugging Techniques

### Enable Debug Logging

**Enable in repository:**
1. Settings → Secrets → New secret
2. Name: `ACTIONS_STEP_DEBUG`, Value: `true`

**Enable in workflow:**
```yaml
env:
  ACTIONS_STEP_DEBUG: true
```

### View Detailed Logs

```bash
# Via GitHub CLI
gh run view <run-id> --log

# Watch in real-time
gh run watch

# Download logs
gh run download <run-id>
```

### Add Debug Output

```yaml
- name: Debug info
  run: |
    echo "Event: ${{ github.event_name }}"
    echo "Ref: ${{ github.ref }}"
    echo "Actor: ${{ github.actor }}"
    echo "Runner OS: ${{ runner.os }}"
    env | sort
```

### Test Locally with act

```bash
# Install act
brew install act

# Run workflow
act push

# Run specific job
act -j test

# With secrets
act --secret-file .secrets
```

## Performance Issues

### Slow Workflow

**Optimize dependency installation:**
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'  # Built-in caching

- run: npm ci  # Faster than npm install
```

**Parallelize jobs:**
```yaml
jobs:
  test:
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - run: npm test -- --shard=${{ matrix.shard }}/4
```

**Skip unnecessary steps:**
```yaml
- name: Build
  if: github.event_name != 'pull_request'
  run: npm run build
```

### Rate Limiting

**GitHub API rate limits:**
- `GITHUB_TOKEN`: 1,000 requests/hour per repository
- Personal access token: 5,000 requests/hour

**Solution:**
- Cache API responses
- Batch operations
- Use GraphQL for complex queries

## Concurrency Issues

**Multiple workflows running simultaneously:**

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true  # Cancel old runs
```

**Queue instead of cancel:**
```yaml
concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: false
```

## Environment Issues

**Wrong environment deployed:**
```yaml
jobs:
  deploy:
    environment: ${{ github.ref == 'refs/heads/main' && 'production' || 'staging' }}
```

**Missing environment variables:**
```yaml
- name: Check required vars
  run: |
    : "${API_URL:?API_URL not set}"
    : "${API_KEY:?API_KEY not set}"
  env:
    API_URL: ${{ secrets.API_URL }}
    API_KEY: ${{ secrets.API_KEY }}
```

## Container Issues

**Docker action fails:**
- Ensure Dockerfile is valid
- Check base image is accessible
- Verify entry point script has execute permission

**Example:**
```yaml
jobs:
  container-job:
    runs-on: ubuntu-latest
    container:
      image: node:20
      options: --cpus 1
    steps:
      - run: node --version
```

## Workflow Syntax Errors

**Validate workflow syntax:**

```bash
# Using GitHub CLI
gh workflow view <workflow-name>

# Using actionlint (third-party tool)
brew install actionlint
actionlint .github/workflows/*.yaml
```

**Common syntax issues:**
- Incorrect indentation (use 2 spaces)
- Missing required fields (`name`, `on`, `jobs`)
- Invalid YAML (tabs, special characters)
- Typo in action names or versions

## Getting Help

**Check workflow run annotations:**
- Go to Actions tab
- Click failed run
- Review annotations on changed files

**GitHub Actions logs:**
- Full logs available in workflow run
- Download logs for offline analysis

**Community resources:**
- [GitHub Actions Forum](https://github.community/c/actions)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- GitHub Status Page for service issues
