# Secrets Management Reference

## GCP Secret Manager

### Create Secrets

```bash
# From command line
echo -n "my-secret-value" | gcloud secrets create SECRET_NAME \
  --data-file=- \
  --project=PROJECT_ID

# From file
gcloud secrets create SECRET_NAME \
  --data-file=/path/to/secret.txt \
  --project=PROJECT_ID

# With labels
gcloud secrets create API_KEY \
  --data-file=- \
  --labels=env=production,app=myapp \
  --project=PROJECT_ID
```

### Access Secrets

```bash
# View secret value
gcloud secrets versions access latest --secret=SECRET_NAME

# View specific version
gcloud secrets versions access 1 --secret=SECRET_NAME

# List all secrets
gcloud secrets list --project=PROJECT_ID
```

### Grant Access

```bash
# Grant read access to service account
gcloud secrets add-iam-policy-binding SECRET_NAME \
  --member=serviceAccount:SERVICE_ACCOUNT_EMAIL \
  --role=roles/secretmanager.secretAccessor \
  --project=PROJECT_ID
```

## Firebase Functions Access

### Using Secret Manager

```javascript
const { SecretManagerServiceClient } = require('@google-cloud/secret-manager');

async function getSecret(secretName) {
  const client = new SecretManagerServiceClient();
  const name = `projects/${process.env.GCP_PROJECT}/secrets/${secretName}/versions/latest`;
  
  const [version] = await client.accessSecretVersion({ name });
  return version.payload.data.toString();
}

// Usage
const apiKey = await getSecret('API_KEY');
```

### Using Firebase Config (Deprecated)

```bash
# Set config
firebase functions:config:set api.key="secret-value"

# Get config
firebase functions:config:get

# Access in function
const functions = require('firebase-functions');
const apiKey = functions.config().api.key;
```

## GitHub Secrets (for CI/CD)

### Add Secrets via UI

1. Repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Enter name and value
4. Click "Add secret"

### Add Secrets via GitHub CLI

```bash
# Set secret
gh secret set SECRET_NAME

# Set from file
gh secret set SECRET_NAME < secret.txt

# Set for specific environment
gh secret set SECRET_NAME --env production
```

### Use in Workflows

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: ./deploy.sh
        env:
          API_KEY: ${{ secrets.API_KEY }}
          GCP_SA_KEY: ${{ secrets.GCP_SA_KEY }}
```

## Terraform Secrets

### Define Sensitive Variables

```hcl
variable "database_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}
```

### Create Secrets in Terraform

```hcl
resource "google_secret_manager_secret" "api_key" {
  secret_id = "api-key"
  
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "api_key_version" {
  secret = google_secret_manager_secret.api_key.id
  secret_data = var.api_key
}
```

### Pass Secrets to Resources

```bash
# Via environment variable
export TF_VAR_api_key="secret-value"
terraform apply

# Via command line (not recommended - visible in history)
terraform apply -var="api_key=secret-value"

# Via tfvars file (gitignored)
# secrets.auto.tfvars
api_key = "secret-value"
```

## Best Practices

### Storage

✅ **DO:**
- Use Secret Manager for runtime secrets
- Use GitHub Secrets for CI/CD credentials
- Use `.env` files locally (gitignored)
- Rotate secrets regularly
- Audit secret access logs

❌ **DON'T:**
- Commit secrets to git (even private repos)
- Log secret values
- Share secrets via Slack/email
- Use same secrets across environments
- Store secrets in code or config files

### Access Control

**Principle of least privilege:**
- Grant secret access only to necessary service accounts
- Use separate secrets for each environment
- Regular audit of secret access permissions

```bash
# Check who has access
gcloud secrets get-iam-policy SECRET_NAME

# Remove access
gcloud secrets remove-iam-policy-binding SECRET_NAME \
  --member=serviceAccount:ACCOUNT_EMAIL \
  --role=roles/secretmanager.secretAccessor
```

### Rotation

**Regular rotation strategy:**
```bash
# Add new version
echo -n "new-secret-value" | gcloud secrets versions add SECRET_NAME --data-file=-

# Disable old version
gcloud secrets versions disable VERSION_ID --secret=SECRET_NAME

# Destroy old version (after grace period)
gcloud secrets versions destroy VERSION_ID --secret=SECRET_NAME
```

## Environment Variables

### Local Development (.env file)

```.env
# .env (add to .gitignore)
GCP_PROJECT=my-app-dev
FIREBASE_API_KEY=xyz123
DATABASE_URL=postgres://localhost:5432/db
```

### Environment Configuration File

Create `.env.example` (committed to git):

```.env
# .env.example
GCP_PROJECT=
FIREBASE_API_KEY=
DATABASE_URL=
```

### Load in Node.js

```javascript
require('dotenv').config();

const project = process.env.GCP_PROJECT;
const apiKey = process.env.FIREBASE_API_KEY;
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Permission denied accessing secret | Verify IAM binding with `gcloud secrets get-iam-policy` |
| Secret not found | Check secret name and project ID |
| Old secret value returned | Secret Manager caches; wait or use specific version |
| Rate limit exceeded | Implement caching in application |
