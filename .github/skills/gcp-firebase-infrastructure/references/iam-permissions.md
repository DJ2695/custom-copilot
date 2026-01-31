# IAM & Permissions Reference

## Common IAM Roles

| Role | Purpose | Use Case |
|------|---------|----------|
| `roles/datastore.user` | Firestore access | Cloud Functions accessing Firestore |
| `roles/storage.objectAdmin` | Full Storage access | File upload/download operations |
| `roles/cloudfunctions.invoker` | Invoke functions | Public HTTP functions |
| `roles/cloudfunctions.developer` | Manage functions | CI/CD deployment |
| `roles/secretmanager.secretAccessor` | Read secrets | Functions accessing secrets |

## Granting Permissions via gcloud

### Service Account Permissions

```bash
# Grant role to service account
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member=serviceAccount:SERVICE_ACCOUNT_EMAIL \
  --role=ROLE_NAME

# Example: Grant Firestore access
gcloud projects add-iam-policy-binding my-project \
  --member=serviceAccount:my-app@my-project.iam.gserviceaccount.com \
  --role=roles/datastore.user
```

### Secret Access

```bash
# Grant secret access
gcloud secrets add-iam-policy-binding SECRET_NAME \
  --member=serviceAccount:SERVICE_ACCOUNT_EMAIL \
  --role=roles/secretmanager.secretAccessor \
  --project=PROJECT_ID
```

## Terraform IAM Configuration

### Project-Level IAM

```hcl
resource "google_project_iam_member" "function_invoker" {
  project = var.project_id
  role    = "roles/cloudfunctions.invoker"
  member  = "serviceAccount:${google_service_account.app.email}"
}

resource "google_project_iam_member" "firestore_user" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.app.email}"
}
```

### Service Account Creation

```hcl
resource "google_service_account" "app" {
  account_id   = "my-app-sa"
  display_name = "My App Service Account"
  project      = var.project_id
}

resource "google_service_account_key" "app_key" {
  service_account_id = google_service_account.app.name
}
```

### Secret Access

```hcl
resource "google_secret_manager_secret_iam_member" "secret_access" {
  secret_id = google_secret_manager_secret.api_key.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.app.email}"
}
```

## Best Practices

### Least Privilege Principle

✅ Grant minimum required permissions
✅ Use service accounts for applications
✅ Separate service accounts per service
✅ Regular audit of permissions

❌ Don't use owner/editor roles in production
❌ Don't share service account keys
❌ Don't grant broad permissions "just in case"

### Service Account Management

**Create service account for each major component:**
- `my-app-functions@project.iam.gserviceaccount.com` - Cloud Functions
- `my-app-ci@project.iam.gserviceaccount.com` - CI/CD pipeline
- `my-app-admin@project.iam.gserviceaccount.com` - Administrative tasks

**Key rotation:**
```bash
# Create new key
gcloud iam service-accounts keys create new-key.json \
  --iam-account=SERVICE_ACCOUNT_EMAIL

# After deployment, delete old key
gcloud iam service-accounts keys delete OLD_KEY_ID \
  --iam-account=SERVICE_ACCOUNT_EMAIL
```
